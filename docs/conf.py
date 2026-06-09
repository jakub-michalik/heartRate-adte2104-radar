"""Konfiguracja Sphinx dla dokumentacji heartRate-adte2104-radar."""
import os
import sys

# żeby autodoc widział moduł aplikacji
sys.path.insert(0, os.path.abspath(".."))

# -- Informacje o projekcie ---------------------------------------------------
project = "heartRate-adte2104-radar"
author = "Jakub Michalik"
copyright = "2026, Jakub Michalik"
release = "1.0"
version = "1.0"

# -- Konfiguracja ogólna ------------------------------------------------------
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
language = "pl"

# Linki do zewnętrznej dokumentacji
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Skróty do często linkowanych zasobów producenta / bibliotek
extlinks = {
    "hlk": ("https://www.hlktech.net/index.php?id=%s", "HLK-LD6002 %s"),
    "ghicewind": ("https://github.com/icewind1991/hlk_ld6002%s", "icewind1991/hlk_ld6002%s"),
}

autodoc_member_order = "bysource"
autodoc_default_options = {"members": True, "undoc-members": True}
napoleon_google_docstring = True

# -- Opcje HTML ---------------------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]
html_title = "ADTE2104 Radar — dokumentacja"
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
