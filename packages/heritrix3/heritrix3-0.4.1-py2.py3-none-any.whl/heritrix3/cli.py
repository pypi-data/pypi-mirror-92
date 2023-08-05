"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mheritrix3` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``heritrix3.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``heritrix3.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import click

from .api import HeritrixAPI
from .api import HeritrixAPIError
from .api import disable_ssl_warnings

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


# ---------------------------------------------------------------------------


class HeritrixContext(object):
    def __init__(self, host=None, user=None, passwd=None):
        self.host = host
        self.user = user
        self.passwd = passwd

        self.api = None


pass_heritrix = click.make_pass_decorator(HeritrixContext, ensure=True)


# ---------------------------------------------------------------------------


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-h",
    "--host",
    default="https://localhost:8443/engine",
    show_default=True,
    help="Heritrix base URI",
)
@click.option(
    "-u", "--username", default="admin", show_default=True, help="HTTP Digest Username"
)
@click.option(
    "-p", "--password", default="admin", show_default=True, help="HTTP Digest Password"
)
@click.version_option()
@click.pass_context
def main(ctx, host, username, password):
    """CLI for the Heritrix API."""
    heritrix_conf = HeritrixContext(host=host, user=username, passwd=password)
    ctx.obj = heritrix_conf

    if ctx.invoked_subcommand is not None:
        # disable insecure warnings ...
        disable_ssl_warnings()

        heritrix_conf.api = HeritrixAPI(
            host=heritrix_conf.host,
            user=heritrix_conf.user,
            passwd=heritrix_conf.passwd,
        )


# ---------------------------------------------------------------------------


@main.command("shell", context_settings=CONTEXT_SETTINGS)
@pass_heritrix
@click.pass_context
def main_shell(ctx, heritrix_conf):
    """Open an interactive shell for testing."""
    import code
    import sys
    from pprint import pprint

    import heritrix3

    banner = (
        f"Python {sys.version} on {sys.platform}\n"
        "Context:\n"
        "\tapi - Heritrix API instance\n"
        "\theritrix3 - heritrix3 module\n"
        "\tctx - click context\n"
        "\tpprint - pprint function\n"
    )
    banner = banner.format(sys.version, sys.platform)
    ctx = dict(api=heritrix_conf.api, ctx=ctx, heritrix3=heritrix3, pprint=pprint)
    ctx.update(locals())

    # Try to enable tab completion
    try:
        # readline module is only available on unix systems
        import readline
    except ImportError:
        pass
    else:
        import rlcompleter

        readline.set_completer(rlcompleter.Completer(ctx).complete)
        readline.parse_and_bind("tab: complete")

    code.interact(banner=banner, local=ctx)


# ---------------------------------------------------------------------------


@main.command(context_settings=CONTEXT_SETTINGS)
@click.option("--unbuilt", flag_value=True, default=False)
@click.option("--sorted", flag_value=True, default=False)
@pass_heritrix
def list_jobs(heritrix_conf, unbuilt, sorted):
    """List jobs, allow filtering for unbuilt ones."""
    api = heritrix_conf.api

    try:
        jobs = api.list_jobs(unbuilt=unbuilt)
    except HeritrixAPIError as ex:
        click.echo(f"Error: {ex}", err=True)
        raise click.Abort()

    if sorted:
        jobs = sorted(jobs)

    for job in jobs:
        click.echo(job)


@main.command(context_settings=CONTEXT_SETTINGS)
@click.option("--sorted", flag_value=True, default=False)
@pass_heritrix
def list_jobs_actions(heritrix_conf, sorted):
    """List jobs and available heritrix actions."""
    api = heritrix_conf.api

    try:
        jobs = api.list_jobs()
    except HeritrixAPIError as ex:
        click.echo(f"Error: {ex}", err=True)
        raise click.Abort()

    if sorted:
        jobs = sorted(jobs)

    jobs_data = list()
    for job_name in jobs:
        try:
            actions = api.get_job_actions(job_name)
            jobs_data.append((job_name, actions))
        except HeritrixAPIError:
            jobs_data.append((job_name, "error"))

    for job, actions in jobs_data:
        actions = "\n * ".join(actions)
        actions = f" * {actions}"
        click.echo(f"{job}\n{actions}")


@main.command(context_settings=CONTEXT_SETTINGS)
@click.argument("jobname", required=False)
@click.option(
    "--raw", flag_value=True, default=False, help="Output plain XML response."
)
@pass_heritrix
def info(heritrix_conf, jobname, raw):
    """Show information about all jobs or a single job.
    If given a jobname as argument then only display information about this job.
    Tries to use ``pygments`` to colorize the output."""
    import json

    api = heritrix_conf.api

    try:
        if raw:
            info = api.info(job_name=jobname, raw=True).text
        else:
            info = api.info(job_name=jobname, raw=False)
            info = json.dumps(info, indent=2)
    except HeritrixAPIError as ex:
        click.echo(f"Error: {ex}", err=True)
        raise click.Abort()

    if raw:
        try:
            from pygments import highlight
            from pygments.formatters import TerminalFormatter
            from pygments.lexers import XmlLexer

            info = highlight(info, XmlLexer(), TerminalFormatter())
        except ImportError:
            pass
    else:
        try:
            from pygments import highlight
            from pygments.formatters import TerminalFormatter
            from pygments.lexers import JsonLexer

            info = highlight(info, JsonLexer(), TerminalFormatter())
        except ImportError:
            pass

    click.echo(info)


# ---------------------------------------------------------------------------
