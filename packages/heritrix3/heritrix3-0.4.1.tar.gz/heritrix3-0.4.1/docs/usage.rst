=====
Usage
=====

To use Heritrix3 Client in a project::

	import heritrix3

A basic workflow follows:

.. code-block:: python

	# basic imports
	from pathlib import Path
	from pprint import pprint
	from heritrix3 import disable_ssl_warnings
	from heritrix3 import HeritrixAPI

	# disable insecure requests warning
	disable_ssl_warnings()

	# create the REST API client
	api = HeritrixAPI(host="https://localhost:8443/engine", user="admin", passwd="admin", verbose=True)

	# dump info
	pprint(api.info(raw=False))
	# similar to info (output wise)
	pprint(api.rescan(raw=False))
	# alternative also
	pprint(HeritrixAPI._xml2json(api.rescan(raw=True).text))

How to work with jobs:

.. code-block:: python

	# create job (if it exists, it will not do anything?)
	jobname = "test"
	pprint(api.create(jobname))
	assert jobname in api.list_jobs()

	# list all jobs
	api.list_jobs()
	# and their actions
	api.get_job_actions(jobname)

	# send a config file (that allows a separate seeds.txt file)
	p = (Path.cwd() / "..").resolve() / "examples" / "crawler-beans.seed_file.cxml"
	api.send_config(jobname, p)

	# create + send seeds
	p = (Path.cwd() / "..").resolve() / "examples" / "seeds.txt"
	p.write_text("https://www.google.com/\n")
	api.send_file(jobname, p)  # or with "seeds.txt" as third param

	# build job (required for some functions, like script execution)
	pprint(api.build(jobname))
	# can be used to wait until an action is available
	# might block indefinitely if this actions does not exists or won't ever be available
	api.wait_for_action(jobname, "launch")

	# launch the job
	pprint(api.launch(jobname))
	# pause a job
	pprint(api.pause(jobname))
	# checkpoint
	pprint(api.checkpoint(jobname))
	# unpause a job
	pprint(api.unpause(jobname))
	# terminate the job
	pprint(api.terminate(jobname))

	# unbuild/teardown the job
	pprint(api.teardown(jobname))

	# NOTE: the following requires the job to be built! (so no teardown)
	# clean up the job (all files are gone)
	# NOTE: you should be careful that the job is not still running
	api.delete_job_dir(jobname)
	pprint(api.rescan())
	assert jobname not in api.list_jobs()

See the official `Heritrix REST API docs <https://heritrix.readthedocs.io/en/latest/>`_.

Show job information:

.. code-block:: python

	job_info_dict = api.info(jobname)
	job_xml_txt = api.info(jobname, raw=True).text

	config_xml_txt = api.get_config(jobname)

	# crawl report (plain text)
	launchid = None  # "latest"
	report_txt = api.crawl_report(jobname, launchid)

	# the following functions require the job to be built

	# list the jobs files
	pprint(api.list_files(jobname))

	# show the warcs (after pause/terminate)
	pprint(api.list_warcs(jobname))

	# launch id
	launchid = api.get_launchid(jobname)



If you require a basic heritrix setup, you may use the
`ekoerner/heritrix <https://hub.docker.com/r/ekoerner/heritrix>`_
Docker image.

CLI
---

The Heritrix3 client library also provides a commandline utility,
named :command:`heritrix3`::

	heritrix3 --help
	# configure your heritrix REST endpoint:
	heritrix3 --host https://localhost:8443/engine --username admin --password admin

	# interactive python shell
	heritrix3 shell

	# list jobs, actions
	heritrix3 list-jobs
	heritrix3 list-jobs-actions

	# show info
	heritrix3 info
	# show job info for "test"
	heritrix3 info test
