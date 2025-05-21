# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath('../../anlagenbetreiber/src/anlagenbetreiber_services'))
sys.path.insert(0, os.path.abspath('../../anlagenbetreiber/src/anlagenbetreiber'))
sys.path.insert(0, os.path.abspath('../../dienstleister/src/dienstleister_services'))
sys.path.insert(0, os.path.abspath('../../dienstleister/src/dienstleister'))
sys.path.insert(0, os.path.abspath('../../hersteller/src/hersteller_services'))
sys.path.insert(0, os.path.abspath('../../hersteller/src/hersteller'))

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Openhub-Demo'
copyright = '2025, Alexander Nasuta, Mats Gesenhues'
author = 'Alexander Nasuta, Mats Gesenhues'
release = '0.1'
language = 'en'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.duration",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autodoc",
]


add_module_names = False

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ["custom.css"]

