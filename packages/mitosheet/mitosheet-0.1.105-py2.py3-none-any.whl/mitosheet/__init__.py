#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
The Mito package, which contains functions for creating a Mito sheet. 

To generate a new sheet, simply run:

import mitosheet
mitosheet.sheet()

If running mitosheet.sheet() just prints text that looks like `MitoWidget(...`, then you need to 
install the JupyterLab extension manager by running:

jupyter labextension install @jupyter-widgets/jupyterlab-manager@2;

Run this command in the terminal where you installed Mito. It should take 5-10 minutes to complete.

Then, restart your JupyterLab instance, and refresh your browser. Mito should now render.

NOTE: if you have any issues with installation, please email book a demo time at https://calendly.com/trymito/mito-early-access-demo?utm_source=moddocstring
"""

import pandas as pd
from mitosheet.example import MitoWidget, sheet
from mitosheet.errors import CreationError, EditError
from mitosheet._version import __version__, version_info

# Export all the sheet functions
from mitosheet.sheet_functions import *
# And the functions for changing types
from mitosheet.sheet_functions.types import *

from .nbextension import _jupyter_nbextension_paths

if __name__ == 'mitosheet':
    import mitosheet.mito_analytics # If the module is imported directly, we log there was an import
    from mitosheet.utils import is_imported_correctly
    from mitosheet.mito_analytics import is_local_deployment

    # We check local deployment first, as this hopefully short curcits and saves us time
    if is_local_deployment() and not is_imported_correctly():
        print("It looks like Mito is incorrectly installed. To finish installing Mito, run:\n\n   jupyter labextension install @jupyter-widgets/jupyterlab-manager@2\n\nRun the above command where you ran `pip install mitosheet`.\n\nThen, you can create a Mito sheet in this notebook with `mitosheet.sheet()`.\n\nIf you want help installing Mito, you can book a demo of the tool at: https://calendly.com/trymito/mito-early-access-demo?utm_source=initprint")
    import mitosheet.mito_analytics