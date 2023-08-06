// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
Contains useful selectors and helpers for adding a new column (and setting it's formula).
*/

import { Selector } from "testcafe";
import { DELETE_PRESS_KEYS_STRING } from "./helpers";
import { getActiveElement, getCellSelector } from "./selectors";

export const columnControlPanelColumnHeaderSelector = Selector('p.column-name-card-column-header');

export const addColumnButton = Selector('div')
    .withExactText('Add Column')
    .parent()

/* 
    Helper function that returns a selector for the given
    columnHeader container - which is the entire box for the column header
    (includes the name and the filter).
*/
export const getColumnHeaderContainerSelector = (columnHeader: string): Selector => {    
    return Selector('div.ag-header-cell')
        .withAttribute('col-id', columnHeader)
}

/* 
    Helper function that returns a selector for the given
    columnHeader - but just the name (what you click to change)
    the name.
*/
export const getColumnHeaderNameSelector = (columnHeader: string): Selector => {    
    return Selector('div.column-header-column-header')
        .withExactText(columnHeader);
}


export const getColumnHeaderFilterSelector = (columnHeader: string): Selector => {
    return getColumnHeaderContainerSelector(columnHeader)
        .find('div.column-header-filter-button')
}


/*
    Sets a a formula at the given columnHeader, row to the correct value
*/
export async function setFormula(t: TestController, formula: string, columnHeader: string, row: string, addColumn?: boolean): Promise<void> {
    if (addColumn !== undefined && addColumn) {
        await t.click(addColumnButton)
        // TODO: check that the added column has the correct column header

    } 

    const cell = getCellSelector(columnHeader, row);

    await t
        .click(cell)
        .pressKey('enter')
        .selectText(Selector('input.ag-cell-inline-editing'))
        // NOTE: somehow, this deletes whatever formula is there, no matter how
        // long the formula is... I'll take it!
        .pressKey(DELETE_PRESS_KEYS_STRING) 
        .typeText(Selector('input.ag-cell-inline-editing'), formula)
        .pressKey('enter')
}

/*
    Sets a a formula at the given columnHeader, row to the correct value
*/
export async function renameColumn(t: TestController, oldColumnHeader: string, newColumnHeader: string): Promise<void> {
    await t
        .click(getColumnHeaderNameSelector(oldColumnHeader))
        .pressKey(DELETE_PRESS_KEYS_STRING)
        .typeText(getActiveElement(), newColumnHeader)
        .pressKey('enter')
}