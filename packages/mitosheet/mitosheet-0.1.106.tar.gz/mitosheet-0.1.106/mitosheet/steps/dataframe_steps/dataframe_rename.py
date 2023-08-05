#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A rename dataframe step changes the name of a specific dataframe
at a specific index.
"""

from mitosheet.utils import make_valid_header
from mitosheet.steps.dataframe_steps.dataframe_duplicate import get_first_unused_name

DATAFRAME_RENAME_EVENT = 'dataframe_rename_edit'
DATAFRAME_RENAME_STEP_TYPE = 'dataframe_rename'

DATAFRAME_RENAME_PARAMS = [
    'sheet_index',
    'old_dataframe_name', # this is saturated 
    'new_dataframe_name'
]

def get_valid_python_variable_name(suggested_dataframe_name):
    """
    Turns the suggested dataframe name into a valid Python identifier.
    """
    # See: https://www.w3schools.com/python/ref_string_isidentifier.asp
    if suggested_dataframe_name.isidentifier():
        return suggested_dataframe_name

    # First, we try and just fill in the non valid characters (like a column header)
    valid_header_version = make_valid_header(suggested_dataframe_name)
    if valid_header_version.isidentifier():
        return valid_header_version

    # Finially prefix with df, so that it doesn't start with a number (as vars cannot)
    return f'df_{valid_header_version}'


def get_valid_dataframe_name(df_names, suggested_dataframe_name):
    """
    Given an attempt at a dataframe name, makes sure that is a valid
    dataframe name (e.g. it is a valid Python identifier, and it is
    not a duplicate).
    """
    valid_identifier = get_valid_python_variable_name(suggested_dataframe_name)
    return get_first_unused_name(df_names, valid_identifier)

def saturate_dataframe_rename(
        wsc,
        event
    ):
    """
    Saturates the dataframe_rename_edit, by adding the old_dataframe_name
    to the event.
    """
    sheet_index = event['sheet_index']
    old_dataframe_name = wsc.curr_step['df_names'][sheet_index]
    event['old_dataframe_name'] = old_dataframe_name


def execute_dataframe_rename(
        wsc,
        sheet_index,
        old_dataframe_name,
        new_dataframe_name
    ):
    """
    Actually performs the exection by creating a new step, and performing the
    dataframe rename in this new step.

    NOTE: this step does it best not to fail and cause annoying errors, 
    as annoying errors are annoying. So, if the given new_dataframe_name is
    invalid in any way, it will correct it to a valid dataframe name. 
    """

    # Bail early, if there is no change
    if old_dataframe_name == new_dataframe_name:
        return

    # Create a new step and save the parameters
    wsc._create_and_checkout_new_step(DATAFRAME_RENAME_STEP_TYPE)

    # Save the parameters
    wsc.curr_step['sheet_index'] = sheet_index
    wsc.curr_step['old_dataframe_name'] = old_dataframe_name
    wsc.curr_step['new_dataframe_name'] = new_dataframe_name

    wsc.curr_step['df_names'][sheet_index] = get_valid_dataframe_name(wsc.curr_step['df_names'], new_dataframe_name)

def transpile_dataframe_rename(
        widget_state_container,
        step,
        sheet_index,
        old_dataframe_name,
        new_dataframe_name
    ):
    """
    Transpiles as dataframe_rename step
    """

    return [f'{step["df_names"][sheet_index]} = {old_dataframe_name}']

DATAFRAME_RENAME_STEP = {
    'step_version': 1,
    'event_type': DATAFRAME_RENAME_EVENT,
    'step_type': DATAFRAME_RENAME_STEP_TYPE,
    'params': DATAFRAME_RENAME_PARAMS,
    'saturate': saturate_dataframe_rename,
    'execute': execute_dataframe_rename,
    'transpile': transpile_dataframe_rename
}