"""Sphinx configuration for the heartRate-adte2104-radar documentation."""
import os
import sys

# so autodoc can see the application module
sys.path.insert(0, os.path.abspath(".."))

# -- Project information ------------------------------------------------------
project = "heartRate-adte2104-radar"
author = "Jakub Michalik"
copyright = "2026, Jakub Michalik"
release = "1.0"
version = "1.0"

# -- General configuration ----------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
language = "en"

# Links to external documentation
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Shortcuts to frequently linked vendor / library resources
extlinks = {
    "hlk": ("https://www.hlktech.net/index.php?id=%s", "HLK-LD6002 %s"),
    "ghicewind": ("https://github.com/icewind1991/hlk_ld6002%s", "icewind1991/hlk_ld6002%s"),
}

autodoc_member_order = "bysource"
autodoc_default_options = {"members": True, "undoc-members": True}
napoleon_google_docstring = True

# -- HTML options -------------------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]
html_title = "ADTE2104 Radar — documentation"
html_theme_options = {
    "source_repository": "https://github.com/jakub-michalik/heartRate-adte2104-radar",
    "source_branch": "main",
    "source_directory": "docs/",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/jakub-michalik/heartRate-adte2104-radar",
            "html": "",
            "class": "fa-brands fa-github",
        },
    ],
}
