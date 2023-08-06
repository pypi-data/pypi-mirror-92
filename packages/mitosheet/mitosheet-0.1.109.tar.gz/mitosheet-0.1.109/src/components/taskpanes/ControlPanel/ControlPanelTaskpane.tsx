// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { ColumnType } from '../../Mito';

// import css
import "../../../../css/margins.css";
import "../../../../css/filter_modal.css";
import "../../../../css/default-taskpane.css";
import "../../../../css/control-panel-taskpane.css"

import { TaskpaneInfo } from '../taskpanes';
import FilterCard, { FiltersTypes } from './FilterCard';
import SortCard from './SortCard';
import ColumnNameCard from './ColumnNameCard';
import { MitoAPI } from '../../../api';


type ControlPanelTaskpaneProps = {
    selectedSheetIndex: number,
    columnHeader: string,
    openEditingColumnHeader: boolean,
    filters: FiltersTypes,
    columnType: ColumnType;
    operator: 'And' | 'Or',
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void,
    mitoAPI: MitoAPI,
}


/*
    A modal that allows a user to rename, sort, and filter a column.
*/
function ControlPanelTaskpane(props: ControlPanelTaskpaneProps): JSX.Element {
    return (
        <div className='control-panel-taskpane-container default-taskpane-div'>
            <ColumnNameCard
                columnHeader={props.columnHeader}
                openEditingColumnHeader={props.openEditingColumnHeader}
                selectedSheetIndex={props.selectedSheetIndex}
                mitoAPI={props.mitoAPI}
                setCurrOpenTaskpane={props.setCurrOpenTaskpane}
            />
            <SortCard
                selectedSheetIndex={props.selectedSheetIndex}
                columnHeader={props.columnHeader} 
                columnType={props.columnType} 
                mitoAPI={props.mitoAPI}
            />
            <FilterCard
                selectedSheetIndex={props.selectedSheetIndex}
                columnHeader={props.columnHeader}
                filters={props.filters}
                columnType={props.columnType}
                operator={props.operator}
                mitoAPI={props.mitoAPI}
            />
        </div>  
    );
}

export default ControlPanelTaskpane;