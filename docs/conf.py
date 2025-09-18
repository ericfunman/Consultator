# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Ajouter le chemin du projet pour les imports
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Consultator"
copyright = "2025, Eric Lapina"
author = "Eric Lapina"
release = "1.0"
version = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # Génération automatique depuis docstrings
    "sphinx.ext.autosummary",  # Tables des matières automatiques
    "sphinx.ext.doctest",  # Tests dans la documentation
    "sphinx.ext.intersphinx",  # Liens vers autres documentations
    "sphinx.ext.todo",  # Support des TODOs
    "sphinx.ext.coverage",  # Couverture de documentation
    "sphinx.ext.imgmath",  # Mathématiques
    "sphinx.ext.mathjax",  # MathJax pour les maths
    "sphinx.ext.ifconfig",  # Configuration conditionnelle
    "sphinx.ext.viewcode",  # Liens vers le code source
    "sphinx.ext.githubpages",  # Support GitHub Pages
    "sphinx_autodoc_typehints",  # Types hints dans l'autodoc
    "sphinx_copybutton",  # Bouton copier dans les exemples de code
    "myst_parser",  # Support Markdown
    "sphinx_design",  # Grilles et cartes
    "sphinxcontrib.httpdomain",  # Documentation API HTTP
]

# Extensions pour le parsing Markdown
source_suffix = {
    ".rst": None,
    ".md": "myst_parser.sphinx_",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "fr"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Configuration du thème RTD
html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "#1f77b4",  # Couleur principale de Consultator
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "streamlit": ("https://docs.streamlit.io/", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/en/14/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True

# -- Options for autodoc extension -------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "member-order": "bysource",
    "special-members": "__init__",
}

autodoc_typehints = "description"
autoclass_content = "both"

# -- Options for autosummary extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html#configuration

autosummary_generate = True

# -- Options for MyST Parser ------------------------------------------------
# https://myst-parser.readthedocs.io/en/latest/configuration.html

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# -- Custom CSS -------------------------------------------------------------
html_css_files = [
    "custom.css",
]
