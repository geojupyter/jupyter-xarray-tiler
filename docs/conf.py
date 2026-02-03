# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
from pathlib import Path

sys.path.insert(0, Path("..").resolve())

project = "jupyter-xarray-tiler"
copyright = "2026, GeoJupyter"  # noqa: A001
author = "GeoJupyter Community"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

nitpicky = True
nitpick_ignore = [
    (
        "py:class",
        "titiler.core.algorithm.base.BaseAlgorithm",
    ),  # TiTiler's docs don't include this
]

extensions = [
    "sphinx.ext.autodoc",  # Generate docs from docstrings
    "sphinx.ext.intersphinx",  # Link to other projects' docs
    "sphinx.ext.napoleon",  # Support Google-style docstrings
    "sphinx.ext.viewcode",  # Add links to source code
    "sphinx_tabs.tabs",  # Support for tabbed "cards"
    "myst_parser",  # Parse Markdown files
]

intersphinx_mapping = {
    "titiler": ("https://developmentseed.org/titiler/", None),
    "xarray": ("https://docs.xarray.dev/en/stable/", None),
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False

myst_enable_extensions = [
    "colon_fence",
]

exclude_patterns = [
    "README.md",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "logo": {
        "text": "jupyter-xarray-tiler",
    },
    "github_url": "https://github.com/geojupyter/jupyter-xarray-tiler",
    "use_edit_page_button": True,
    "show_prev_next": False,
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
}

html_context = {
    "github_user": "geojupyter",
    "github_repo": "jupyter-xarray-tiler",
    "github_version": "main",
    "doc_path": "docs/source",
}

# -- Autodoc Options ---------------------------------------------------------
# Ensure methods are documented
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
}
