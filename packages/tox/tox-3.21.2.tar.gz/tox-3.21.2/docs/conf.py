import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from docutils import nodes
from sphinx import addnodes

import tox

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinxcontrib.autoprogram",
]
ROOT_SRC_TREE_DIR = Path(__file__).parents[1]


def generate_draft_news():
    home = "https://github.com"
    issue = "{}/issue".format(home)
    fragments_path = ROOT_SRC_TREE_DIR / "docs" / "changelog"
    for pattern, replacement in (
        (r"[^`]@([^,\s]+)", r"`@\1 <{}/\1>`_".format(home)),
        (r"[^`]#([\d]+)", r"`#pr\1 <{}/\1>`_".format(issue)),
    ):
        for path in fragments_path.glob("*.rst"):
            path.write_text(re.sub(pattern, replacement, path.read_text()))
    env = os.environ.copy()
    env["PATH"] += os.pathsep.join(
        [os.path.dirname(sys.executable)] + env["PATH"].split(os.pathsep),
    )
    changelog = subprocess.check_output(
        ["towncrier", "--draft", "--version", "DRAFT"],
        cwd=str(ROOT_SRC_TREE_DIR),
        env=env,
    ).decode("utf-8")
    if "No significant changes" in changelog:
        content = ""
    else:
        note = "*Changes in master, but not released yet are under the draft section*."
        content = "{}\n\n{}".format(note, changelog)
    (ROOT_SRC_TREE_DIR / "docs" / "_draft.rst").write_text(content)


generate_draft_news()

project = u"tox"
_full_version = tox.__version__
release = _full_version.split("+", 1)[0]
version = ".".join(release.split(".")[:2])

author = "holger krekel and others"
year = date.today().year
copyright = u"2010-{}, {}".format(year, author)

master_doc = "index"
source_suffix = ".rst"

exclude_patterns = ["changelog/*"]

templates_path = ["_templates"]
pygments_style = "sphinx"

html_theme = "alabaster"
html_theme_options = {
    "logo": "img/tox.png",
    "github_user": "tox-dev",
    "github_repo": "tox",
    "description": "standardise testing in Python",
    "github_banner": "true",
    "github_type": "star",
    "travis_button": "false",
    "badge_branch": "master",
    "fixed_sidebar": "false",
}
html_sidebars = {
    "**": ["about.html", "localtoc.html", "relations.html", "searchbox.html", "donate.html"],
}
html_show_sourcelink = False
html_static_path = ["_static"]
htmlhelp_basename = "{}doc".format(project)
latex_documents = [("index", "tox.tex", u"{} Documentation".format(project), author, "manual")]
man_pages = [("index", project, u"{} Documentation".format(project), [author], 1)]
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

intersphinx_mapping = {"https://docs.python.org/": None}


def setup(app):
    def parse_node(env, text, node):
        args = text.split("^")
        name = args[0].strip()

        node += addnodes.literal_strong(name, name)

        if len(args) > 2:
            default = "={}".format(args[2].strip())
            node += nodes.literal(text=default)

        if len(args) > 1:
            content = "({})".format(args[1].strip())
            node += addnodes.compact_paragraph(text=content)

        return name  # this will be the link

    app.add_object_type(
        directivename="conf",
        rolename="conf",
        objname="configuration value",
        indextemplate="pair: %s; configuration value",
        parse_node=parse_node,
    )


tls_cacerts = os.getenv("SSL_CERT_FILE")  # we don't care here about the validity of certificates
linkcheck_timeout = 30
linkcheck_ignore = [r"https://holgerkrekel.net"]

extlinks = {
    "issue": ("https://github.com/tox-dev/tox/issues/%s", "#"),
    "pull": ("https://github.com/tox-dev/tox/pull/%s", "p"),
    "user": ("https://github.com/%s", "@"),
}
