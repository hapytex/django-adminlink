# Configuration file for the Sphinx documentation builder.

# -- Project information

import django
from sys import path
from os.path import dirname
from os import environ

project = "django-adminlink"
copyright = "2025, Willem Van Onsem"
author = "Willem Van Onsem"

release = "0.2.0"
version = "0.2.0"


path.insert(0, dirname(dirname(dirname(__file__))))
environ.setdefault("DJANGO_SETTINGS_MODULE", "docs.source.settings")


django.setup()

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

# html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = "footnote"
