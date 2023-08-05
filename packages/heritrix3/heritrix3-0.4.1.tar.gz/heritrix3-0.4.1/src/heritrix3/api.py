import os
import time
from typing import Any
from typing import BinaryIO
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import requests
from lxml import etree
from requests.auth import HTTPDigestAuth

# ---------------------------------------------------------------------------

__all__ = ["HeritrixAPIError", "HeritrixAPI"]

#: default chunk/buffer size for downloading is 16kB
CHUNKSIZE = 16 * 1024

# ---------------------------------------------------------------------------


def disable_ssl_warnings():
    """Quieten SSL insecure warnings.

    See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
    """
    import urllib3

    urllib3.disable_warnings()


# ---------------------------------------------------------------------------


class HeritrixAPIError(Exception):
    """Error as response from Heritrix3 REST API.

    Arguments
    ---------
    message : str
        Error description / message.
    response : Optional[requests.Response]
        Optional api response object.
    """

    def __init__(self, message: str, *args, **kwargs):
        self.message = message
        self.response: Optional[requests.Response] = kwargs.pop("response", None)
        super(HeritrixAPIError, self).__init__(message, *args, **kwargs)

    def __str__(self) -> str:
        return f"HeritrixAPIError: {self.message}"


# ---------------------------------------------------------------------------


class HeritrixAPI:
    def __init__(
        self,
        host: str = "https://localhost:8443/engine",
        user: str = "admin",
        passwd: str = "admin",
        verbose: bool = False,
        insecure: bool = True,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[Union[int, float]] = None,
    ):
        self.host: str = host
        self.auth = HTTPDigestAuth(user, passwd)
        self.verbose = verbose
        self.insecure = insecure
        self.timeout = timeout

        # strip trailing slashes
        if self.host:
            self.host = self.host.rstrip("/")

        self.headers: Dict[str, str] = {"Accept": "application/xml"}

        if isinstance(headers, dict):
            self.headers.update(headers)

        self.last_response: Optional[requests.Response] = None

    # --------------------------------
    # api requests

    def _post(
        self,
        url: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        code: Optional[int] = None,
        timeout: Optional[Union[int, float]] = None,
        raw: bool = True,
    ) -> Union[str, requests.Response]:
        if not url:
            url = self.host

        headers_copy = dict(self.headers)
        if headers is not None:
            headers_copy.update(headers)

        if data is None:
            data = dict()

        resp = requests.post(
            url,
            auth=self.auth,
            data=data,
            headers=headers_copy,
            verify=not self.insecure,
            timeout=self.timeout if timeout is None else timeout,
        )
        self.last_response = resp

        if code is not None and resp.status_code != code:
            raise HeritrixAPIError(
                f"Invalid response code: expected: {code}, got: {resp.status_code}, url={url}"
            )

        if not raw:
            resp = self._xml2json(resp.text)

        return resp

    def _get(
        self,
        url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        api_headers: Optional[Dict[str, str]] = True,
        code: Optional[int] = None,
        timeout: Optional[Union[int, float]] = None,
        raw: bool = True,
    ) -> Union[str, requests.Response]:
        if not url:
            url = self.host

        headers_copy = dict()
        if api_headers:
            headers_copy.update(self.headers)
        if headers is not None:
            headers_copy.update(headers)

        resp = requests.get(
            url,
            auth=self.auth,
            headers=headers_copy,
            verify=not self.insecure,
            timeout=self.timeout if timeout is None else timeout,
        )
        self.last_response = resp

        if code is not None and resp.status_code != code:
            raise HeritrixAPIError(
                f"Invalid response code: expected: {code}, got: {resp.status_code}; url={url}"
            )

        if not raw:
            resp = self._xml2json(resp.text)

        return resp

    def _post_action(
        self,
        action: str,
        url: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        code: Optional[int] = None,
        raw: bool = True,
    ) -> Union[str, requests.Response]:
        if not action:
            raise ValueError("Missing action.")

        if data is None:
            data = dict()

        data["action"] = action

        return self._post(url=url, data=data, headers=headers, code=code, raw=raw)

    def _job_action(
        self,
        action: str,
        job_name: str,
        data: Optional[Dict[str, Any]] = None,
        code: Optional[int] = None,
        raw: bool = True,
    ) -> Union[str, requests.Response]:
        if not job_name:
            raise ValueError("Missing job name.")

        url = f"{self.host}/job/{job_name}"

        return self._post_action(action, url, data=data, code=code, raw=raw)

    # --------------------------------
    # upload/download

    def send_file(
        self, job_name: str, filepath: os.PathLike, name: Optional[str] = None
    ) -> bool:
        if not job_name:
            raise ValueError("Missing job name.")
        if not filepath:
            raise ValueError("Missing filepath.")
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            raise FileNotFoundError(filepath)

        if not name:
            name = os.path.basename(filepath)
        url = f"{self.host}/job/{job_name}/jobdir/{name}"

        with open(filepath, "rb") as fdat:
            resp = requests.put(
                url,
                auth=self.auth,
                data=fdat,
                headers=self.headers,
                verify=not self.insecure,
            )
        return resp.ok

    def send_content(
        self, job_name: str, filecontent: Union[bytes, BinaryIO], name: str
    ) -> bool:
        if not job_name:
            raise ValueError("Missing job name.")
        if not name:
            raise ValueError("Missing (upload file) name.")

        url = f"{self.host}/job/{job_name}/jobdir/{name}"

        resp = requests.put(
            url,
            auth=self.auth,
            data=filecontent,
            headers=self.headers,
            verify=not self.insecure,
        )
        return resp.ok

    def retrieve_file(
        self,
        job_name: str,
        local_filepath: os.PathLike,
        job_filepath: Union[str, os.PathLike],
        overwrite: bool = False,
    ) -> bool:
        if not job_name:
            raise ValueError("Missing job name.")
        if not local_filepath:
            raise ValueError("Missing local_filepath.")
        if not overwrite and (
            os.path.exists(local_filepath) or os.path.isfile(local_filepath)
        ):
            raise FileExistsError(local_filepath)
        if not job_filepath:
            raise ValueError("Missing job_filepath.")

        prefix = f"./jobs/{job_name}/"
        if job_filepath.startswith(prefix):
            job_filepath = job_filepath[len(prefix) :]  # noqa: E203

        url = f"{self.host}/job/{job_name}/jobdir/{job_filepath}"

        # see: https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
        with requests.get(
            url,
            auth=self.auth,
            headers=self.headers,
            verify=not self.insecure,
            stream=True,
        ) as resp:
            if resp.ok:
                with open(local_filepath, "wb") as fp:
                    for chunk in resp.iter_content(chunk_size=CHUNKSIZE):
                        fp.write(chunk)
                    # shutil.copyfileobj(resp.raw, fp)

        return resp.ok

    # --------------------------------

    def info(
        self, job_name: Optional[str] = None, raw: bool = False
    ) -> Union[str, requests.Response]:
        url = None
        if job_name is not None:
            url = f"{self.host}/job/{job_name}"

        resp = self._get(url=url, code=200, raw=raw)

        return resp

    def list_jobs(
        self, status: Optional[str] = None, unbuilt: bool = False
    ) -> List[str]:
        resp: requests.Response = self._get(raw=True)
        xml_doc = etree.fromstring(resp.text)

        if unbuilt:
            # if unbuilt, then search for those only
            jobs = xml_doc.xpath("//jobs/value[./statusDescription = 'Unbuilt']")
        elif status is not None:
            # then search for crawlControllerState
            jobs = xml_doc.xpath(f"//jobs/value[./crawlControllerState = '{status}']")
        else:
            # else all
            jobs = xml_doc.xpath("//jobs/value")

        job_names = [job.find("shortName").text for job in jobs]
        return job_names

    def get_job_state(self, job_name: str) -> Optional[str]:
        resp = self.info(job_name=job_name, raw=True)
        xml_doc = etree.fromstring(resp.text)
        state = xml_doc.xpath("/job/crawlControllerState/text()")
        if not state:
            return None
        return state[0]

        # <statusDescription>Finished: FINISHED</statusDescription> # Active: RUNNING
        # https://github.com/internetarchive/heritrix3/blob/adac067ea74b5a89f631ef771e2f598819bac6c4/engine/src/main/java/org/archive/crawler/framework/CrawlJob.java#L971  # noqa: E501

        # <crawlExitStatus>FINISHED</crawlExitStatus> # RUNNING, ...
        # https://github.com/internetarchive/heritrix3/blob/adac067ea74b5a89f631ef771e2f598819bac6c4/engine/src/main/java/org/archive/crawler/framework/CrawlController.java#L265  # noqa: E501
        # -> CrawlStatus
        # -> https://github.com/internetarchive/heritrix3/blob/master/engine/src/main/java/org/archive/crawler/framework/CrawlStatus.java

        # <crawlControllerState>FINISHED</crawlControllerState>
        # only set at end, while running it is empty
        # -> State
        # -> https://github.com/internetarchive/heritrix3/blob/adac067ea74b5a89f631ef771e2f598819bac6c4/engine/src/main/java/org/archive/crawler/framework/CrawlController.java#L267  # noqa: E501

    def get_crawl_exit_state(self, job_name: str) -> Optional[str]:
        resp = self.info(job_name=job_name, raw=True)
        xml_doc = etree.fromstring(resp.text)
        state = xml_doc.xpath("/job/crawlExitStatus/text()")
        if not state:
            return None
        return state[0]

    def get_job_actions(self, job_name: str) -> List[str]:
        # info = self.info(job_name=job_name, raw=False)
        # return info["job"]["availableActions"]["value"]
        resp = self.info(job_name=job_name, raw=True)
        xml_doc = etree.fromstring(resp.text)
        actions = xml_doc.xpath("/job/availableActions/value/text()")
        return actions

    def wait_for_action(
        self,
        job_name: str,
        action: str,
        timeout: Union[int, float] = 20,
        poll_delay: Union[int, float] = 1,
    ) -> bool:
        if poll_delay <= 0:
            raise ValueError("poll_delay mustn't be negative or null!")

        time_start = time.time()

        avail_actions = self.get_job_actions(job_name)
        while action not in avail_actions:
            if timeout is not None and (time.time() - time_start > timeout):
                # raise TimeoutError
                return False

            time.sleep(poll_delay)
            avail_actions = self.get_job_actions(job_name)

        return True

    def wait_for_jobstate(
        self,
        job_name: str,
        state: str,
        timeout: Union[int, float] = 20,
        poll_delay: Union[int, float] = 1,
    ) -> bool:
        if poll_delay <= 0:
            raise ValueError("poll_delay mustn't be negative or null!")

        time_start = time.time()

        current_state = self.get_job_state(job_name)
        while state != current_state:
            if timeout is not None and (time.time() - time_start > timeout):
                # raise TimeoutError
                return False

            time.sleep(poll_delay)
            current_state = self.get_job_state(job_name)

        return True

    # --------------------------------
    # new job

    def create(self, job_name: str, raw: bool = False) -> Union[str, requests.Response]:
        if not job_name:
            raise ValueError("Missing job name.")

        return self._post_action("create", data={"createpath": job_name}, raw=raw)

    def add(self, job_dir: str, raw: bool = False) -> Union[str, requests.Response]:
        if not job_dir:
            raise ValueError("Missing job directory.")
        # TODO: check that a cxml file is in the directory?

        return self._post_action("add", data={"addpath": job_dir}, raw=raw)

    def rescan(self, raw: bool = False) -> Union[str, requests.Response]:
        return self._post_action("rescan", raw=raw)

    def copy(
        self,
        job_name: str,
        new_job_name: str,
        as_profile: bool = False,
        raw: bool = False,
    ) -> Union[str, requests.Response]:
        if not new_job_name:
            raise ValueError("new_job_name must not be empty!")

        data = dict()
        data["copyTo"] = new_job_name
        if as_profile:
            data["as_profile"] = "on"

        return self._job_action("copy", job_name, data=data, raw=raw)

    # --------------------------------
    # job control

    def build(self, job_name: str, raw: bool = False) -> Union[str, requests.Response]:
        return self._job_action("build", job_name, raw=raw)

    def launch(
        self, job_name: str, checkpoint: Optional[str] = None, raw: bool = False
    ) -> Union[str, requests.Response]:
        data = None
        if checkpoint is not None:
            data = {"checkpoint": checkpoint}

        return self._job_action("launch", job_name, data=data, raw=raw)

    def pause(self, job_name: str, raw: bool = False) -> Union[str, requests.Response]:
        return self._job_action("pause", job_name, raw=raw)

    def unpause(
        self, job_name: str, raw: bool = False
    ) -> Union[str, requests.Response]:
        return self._job_action("unpause", job_name, raw=raw)

    def terminate(
        self, job_name: str, raw: bool = False
    ) -> Union[str, requests.Response]:
        return self._job_action("terminate", job_name, raw=raw)

    def teardown(
        self, job_name: str, raw: bool = False
    ) -> Union[str, requests.Response]:
        return self._job_action("teardown", job_name, raw=raw)

    def checkpoint(
        self, job_name: str, raw: bool = False
    ) -> Union[str, requests.Response]:
        return self._job_action("checkpoint", job_name, raw=raw)

    # --------------------------------
    # script execution

    def execute_script(
        self, job_name: str, script: str, engine: str = "beanshell", raw: bool = False
    ) -> Union[str, requests.Response]:
        if not job_name:
            raise ValueError("Missing job name.")
        if not script:
            raise ValueError("Missing script?")
        if engine not in ("beanshell", "js", "groovy", "AppleScriptEngine"):
            raise ValueError(f"Invalid script engine param: {engine}")

        data = dict()
        data["engine"] = engine
        data["script"] = script

        url = f"{self.host}/job/{job_name}/script"

        return self._post(url=url, data=data, raw=raw)

    # --------------------------------
    #  configs

    def get_config(self, job_name: str, raw: bool = True) -> str:
        config_url = self.get_config_url(job_name)

        resp = self._get(url=config_url, code=200, raw=raw)

        return resp.text

    def send_config(self, job_name: str, cxml_filepath: os.PathLike) -> bool:
        if not job_name:
            raise ValueError("Missing job name.")
        if cxml_filepath is None or cxml_filepath == "":
            raise ValueError("Missing cxml filepath name.")
        if not os.path.exists(cxml_filepath) or not os.path.isfile(cxml_filepath):
            raise FileNotFoundError(cxml_filepath)

        # TODO: check config url with :func:`get_config_url()` ?

        return self.send_file(job_name, cxml_filepath, "crawler-beans.cxml")

    def get_config_url(self, job_name: str) -> str:
        if not job_name:
            raise ValueError("Missing job name.")

        resp = self.info(job_name=job_name, raw=True)
        if not resp:
            raise HeritrixAPIError(
                f"Error retrieving job info! {resp.status_code}"
                f" - {resp.reason}, url={resp.url}"
            )

        xml_doc = etree.fromstring(resp.text)
        config_url = xml_doc.xpath("/job/primaryConfigUrl[1]/text()")
        if not config_url:
            raise HeritrixAPIError("Invalid job configuration document?")

        return config_url[0]

    # --------------------------------
    # private: helpers - xml conversion

    @classmethod
    def _xml2json(cls, xml_str: Union[str, "etree._Element"]) -> str:
        if isinstance(xml_str, str):
            xml_doc = etree.fromstring(xml_str)
        elif isinstance(xml_str, etree._Element):
            xml_doc = xml_str
        else:
            raise TypeError(f"Invalid xml_str type, got: {type(xml_str)}")

        return cls.__tree_to_dict(xml_doc)

    @classmethod
    def __tree_to_dict(cls, tree: "etree._Element") -> Dict[str, Any]:
        # see: https://github.com/WilliamMayor/hapy/blob/master/hapy/hapy.py#L213
        if len(tree) == 0:
            return {tree.tag: tree.text}
        D = {}
        for child in tree:
            d = cls.__tree_to_dict(child)
            tag = list(d.keys())[0]
            try:
                try:
                    D[tag].append(d[tag])
                except AttributeError:
                    D[tag] = [D[tag], d[tag]]
            except KeyError:
                D[tag] = d[tag]
        return {tree.tag: D}

    # --------------------------------
    # job infos

    def get_launchid(self, job_name: str) -> Optional[str]:
        script = "rawOut.println( appCtx.getCurrentLaunchId() );"
        resp = self.execute_script(
            job_name, script=script, engine="beanshell", raw=True
        )
        if not resp.ok:
            if resp.status_code == 500:
                # most probably not application context / unbuilt job
                return None

            raise HeritrixAPIError(
                f"No launchid found: {resp.status_code} - {resp.reason}"
            )

        tree = etree.fromstring(resp.text)
        ret = tree.find("rawOutput").text.strip()
        if ret == "null":
            # build but not launched?
            return None
        return ret

    # --------------------------------
    # reports & logs

    def _get_report(
        self,
        job_name: str,
        report_name: str,
        report_meta_name: Optional[str] = None,
        launch_id: Optional[str] = None,
    ) -> Optional[str]:
        if launch_id is None:
            if report_meta_name:
                try:
                    # use meta URL to get latest (disable HTTP caching)
                    url = f"{self.host}/job/{job_name}/report/{report_meta_name}"

                    resp = self._get(url=url, api_headers=False, raw=True)
                    if resp.ok:
                        return resp.text
                except Exception as ex:  # noqa: F841
                    pass

            try:
                # if no launchid - try to get with "latest"
                url = f"{self.host}/job/{job_name}/jobdir/latest/reports/{report_name}"

                resp = self._get(url=url, api_headers=False, raw=True)
                if resp.ok:
                    return resp.text
            except Exception as ex:  # noqa: F841
                pass

            # if that fails, try to query the launch_id and try again
            launch_id = self.get_launchid(job_name)

            if launch_id is None:
                # unbuilt job?
                # either it got anything with latest or there simply was not yet a crawl
                raise HeritrixAPIError(
                    f"Unbuilt Job {job_name}, check if has ever crawled?"
                )

            return self._get_report(
                job_name,
                report_name,
                report_meta_name=report_meta_name,
                launch_id=launch_id,
            )

        # ----------------------------

        url = f"{self.host}/job/{job_name}/jobdir/{launch_id}/reports/{report_name}"

        resp = self._get(url=url, api_headers=False, raw=True)
        if resp.ok:
            return resp.text

        return None

    def _get_log(
        self,
        job_name: str,
        log_name: str,
        launch_id: Optional[str] = None,
    ) -> Optional[str]:
        if launch_id is None:
            try:
                # if no launchid - try to get with "latest"
                url = f"{self.host}/job/{job_name}/jobdir/latest/logs/{log_name}"

                resp = self._get(url=url, api_headers=False, raw=True)
                if resp.ok:
                    return resp.text
            except Exception as ex:  # noqa: F841
                pass

            # if that fails, try to query the launch_id and try again
            launch_id = self.get_launchid(job_name)

            if launch_id is None:
                # unbuilt job?
                # either it got anything with latest or there simply was not yet a crawl
                raise HeritrixAPIError(
                    f"Unbuilt Job {job_name}, check if has ever crawled?"
                )

            return self._get_log(
                job_name,
                log_name,
                launch_id=launch_id,
            )

        # ----------------------------

        url = f"{self.host}/job/{job_name}/jobdir/{launch_id}/logs/{log_name}"

        resp = self._get(url=url, api_headers=False, raw=True)
        if resp.ok:
            return resp.text

        return None

    def crawl_report(
        self, job_name: str, launch_id: Optional[str] = None
    ) -> Optional[str]:
        return self._get_report(
            job_name,
            "crawl-report.txt",
            report_meta_name="CrawlSummaryReport",
            launch_id=launch_id,
        )

    def seeds_report(
        self, job_name: str, launch_id: Optional[str] = None
    ) -> Optional[str]:
        return self._get_report(
            job_name,
            "seeds-report.txt",
            report_meta_name="SeedsReport",
            launch_id=launch_id,
        )

    def hosts_report(
        self, job_name: str, launch_id: Optional[str] = None
    ) -> Optional[str]:
        return self._get_report(
            job_name,
            "hosts-report.txt",
            report_meta_name="HostsReport",
            launch_id=launch_id,
        )

    def mimetypes_report(
        self, job_name: str, launch_id: Optional[str] = None
    ) -> Optional[str]:
        return self._get_report(
            job_name,
            "mimetype-report.txt",
            report_meta_name="MimetypesReport",
            launch_id=launch_id,
        )

    def responsecodes_report(
        self, job_name: str, launch_id: Optional[str] = None
    ) -> Optional[str]:
        return self._get_report(
            job_name,
            "responsecode-report.txt",
            report_meta_name="ResponseCodeReport",
            launch_id=launch_id,
        )

    def job_log(self, job_name: str) -> Optional[str]:
        url = f"{self.host}/job/{job_name}/jobdir/job.log"

        resp = self._get(url=url, api_headers=False, raw=True)
        if resp.ok:
            return resp.text

        return None

    def crawl_log(
        self, job_name: str, launch_id: Optional[str] = None
    ) -> Optional[str]:
        return self._get_log(job_name, log_name="crawl.log", launch_id=launch_id)

    # --------------------------------
    # job files

    def list_files(
        self, job_name: str, gather_files: bool = True, gather_folders: bool = True
    ) -> List[str]:
        script_fileout = """
            it.eachFile {
                rawOut.println( it );
            };
        """.strip()
        if not gather_files:
            script_fileout = ""

        script_folder_out = """
            rawOut.println( it )
        """.strip()
        if not gather_folders:
            script_folder_out = ""

        script = f"""
        def listRecurs;
        listRecurs = {{
            it.eachDir( listRecurs );
            {script_fileout}
            {script_folder_out}
        }};
        listRecurs( job.jobDir )
        """

        resp: requests.Response = self.execute_script(
            job_name, script=script, engine="groovy", raw=True
        )

        if not resp.ok:
            if resp.status_code == 500:
                # most probably not application context / unbuilt job
                return []

            raise HeritrixAPIError(
                f"Error executing listRecurs script: {resp.status_code} - {resp.reason}"
            )

        tree = etree.fromstring(resp.text)
        outtree = tree.find("rawOutput")
        if outtree is None:
            error = "No error output found?!"
            errtree = tree.find("exception")
            if errtree is not None:
                error = errtree.text
            raise HeritrixAPIError(f"Error executing listRecurs script: {error}")

        text = outtree.text.strip()
        lines = [ln.strip() for ln in text.splitlines()]
        return lines

    def list_warcs(
        self, job_name: str, launchid: Optional[str] = None
    ) -> Optional[List[str]]:
        if not launchid:
            launchid = "latest"

        script = f"""
        warcDir = new File( job.jobDir, "{launchid}/warcs" )
        warcDir.eachFile {{
            rawOut.println( it );
        }};
        """.strip()

        resp = self.execute_script(job_name, script=script, engine="groovy", raw=True)

        if not resp.ok:
            if resp.status_code == 500:
                # most probably not application context / unbuilt job
                return []

            raise HeritrixAPIError(
                f"Error executing list_warcs script: {resp.status_code} - {resp.reason}"
            )

        tree = etree.fromstring(resp.text)
        outtree = tree.find("rawOutput")
        if outtree is None:
            error = "No error output found?!"
            errtree = tree.find("exception")
            if errtree is not None:
                error = errtree.text
                # check if path simply does not yet exists for job,
                # then no files, return None
                if (
                    "javax.script.ScriptException: java.io.FileNotFoundException:"
                    in error
                ):
                    return None
            # otherwise other error
            raise HeritrixAPIError(f"Error executing list_warcs script: {error}")

        text = outtree.text.strip()
        lines = [ln.strip() for ln in text.splitlines()]
        return lines

    def retrieve_warcs(
        self,
        job_name: str,
        local_folderpath: os.PathLike,
        launchid: Optional[str] = None,
        warcs_job_filepaths: Optional[List[Union[str, os.PathLike]]] = None,
        overwrite: bool = False,
    ) -> Optional[int]:
        if not job_name:
            raise ValueError("Missing job name.")
        if not local_folderpath:
            raise ValueError("Missing local_folderpath.")
        if not os.path.exists(local_folderpath) or not os.path.isdir(local_folderpath):
            raise FileNotFoundError(local_folderpath)

        if not warcs_job_filepaths:
            # try to query file list from job
            # if it throws an error, forward it to user
            warcs_job_filepaths = self.list_warcs(job_name, launchid=launchid)

        # if None return None to signal no warcs provided and job can't find any?
        if warcs_job_filepaths is None:
            return None
        # will return 0 if empty list (job has nothing crawled as of yet)

        num_ok = num_bad = 0
        for warc_filepath in warcs_job_filepaths:
            warc_name = warc_filepath.rsplit("/", 1)[-1]
            local_filepath = os.path.join(local_folderpath, warc_name)

            # retrieve file
            ok = self.retrieve_file(
                job_name, local_filepath, warc_filepath, overwrite=overwrite
            )
            if ok:
                num_ok += 1
            else:
                num_bad += 1
            # NOW, how to handle errors, abort?
            # continue with next?
            # AND, what to return, count ok, count not ok, raise errors?

        return num_ok

    def delete_job_dir(self, job_name: str) -> None:
        script = """
        def delRecurs;
        delRecurs = {
            it.eachDir( delRecurs );
            it.eachFile {
                it.delete();
            };
            it.delete();
        };
        delRecurs( job.jobDir )
        """

        resp: requests.Response = self.execute_script(
            job_name, script=script, engine="groovy", raw=True
        )

        if not resp.ok:
            raise HeritrixAPIError(
                f"Error executing delRecurs script: {resp.status_code} - {resp.reason}"
            )

    # --------------------------------


# ---------------------------------------------------------------------------
