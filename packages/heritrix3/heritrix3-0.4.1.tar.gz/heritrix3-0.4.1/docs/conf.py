# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_click",
]
source_suffix = ".rst"
master_doc = "index"
project = "Heritrix3 Client"
year = "2021"
author = "Erik Körner"
copyright = "{0}, {1}".format(year, author)
version = release = "0.4.1"

pygments_style = "trac"
templates_path = ["."]
extlinks = {
    "issue": ("https://github.com/Querela/python-heritrix3-client/issues/%s", "#"),
    "pr": ("https://github.com/Querela/python-heritrix3-client/pull/%s", "PR #"),
}
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get("READTHEDOCS", None) == "True"

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = "sphinx_rtd_theme"

html_use_smartypants = True
html_last_updated_fmt = "%b %d, %Y"
html_split_index = False
html_sidebars = {
    "**": ["searchbox.html", "globaltoc.html", "sourcelink.html"],
}
html_short_title = "%s-%s" % (project, version)

autoclass_content = "both"
autodoc_member_order = "bysource"

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False

linkcheck_ignore = [
    # local test urls?
    r"^https://localhost:8443/engine",
]
