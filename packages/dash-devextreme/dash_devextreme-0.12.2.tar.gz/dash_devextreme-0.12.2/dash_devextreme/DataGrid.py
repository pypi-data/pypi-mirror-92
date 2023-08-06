# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DataGrid(Component):
    """A DataGrid component.


Keyword arguments:
- id (string; optional)
- accessKey (string; optional)
- activeStateEnabled (boolean; default False)
- allowColumnReordering (boolean; default False)
- allowColumnResizing (boolean; default False)
- cacheEnabled (boolean; default True)
- cellHintEnabled (boolean; default True)
- columnAutoWidth (boolean; default False)
- columnChooser (dict; optional)
- columnFixing (dict; optional)
- columnHidingEnabled (boolean; default False)
- columnMinWidth (number; optional)
- columnResizingMode (a value equal to: 'nextColumn', 'widget'; default 'nextColumn')
- columns (list of dicts; optional)
- columnWidth (number; optional)
- dataSource (dict | list of dicts; optional)
- dateSerializationFormat (string; optional)
- disabled (boolean; default False)
- editing (dict; optional)
- elementAttr (dict; optional)
- errorRowEnabled (boolean; default True)
- export (dict; optional)
- filterBuilder (dict; optional)
- filterBuilderPopup (dict; optional)
- filterPanel (dict; optional)
- filterRow (dict; optional)
- filterSyncEnabled (boolean; optional)
- filterValue (dict; optional)
- focusedColumnIndex (number; default -1)
- focusedRowEnabled (boolean; default False)
- focusedRowIndex (number; default -1)
- focusedRowKey (boolean | number | string | dict | list; optional)
- focusStateEnabled (boolean; default False)
- grouping (dict; optional)
- groupPanel (dict; optional)
- headerFilter (dict; optional)
- height (number | string; optional)
- highlightChanges (boolean; default False)
- hint (string; optional)
- hoverStateEnabled (boolean; default False)
- keyExpr (string | list of strings; optional)
- loadPanel (dict; optional)
- masterDetail (dict; optional)
- noDataText (string; default 'No data')
- onCellClick (string; optional)
- onRowClick (string; optional)
- pager (dict; optional)
- paging (dict; optional)
- remoteOperations (boolean | dict; optional)
- renderAsync (boolean; default False)
- repaintChangesOnly (boolean; default False)
- rowAlternationEnabled (boolean; default False)
- rowTemplate (string; optional)
- rtlEnabled (boolean; default False)
- scrolling (dict; optional)
- searchPanel (dict; optional)
- selectedRowKeys (list of boolean | number | string | dict | lists; optional)
- selection (dict; optional)
- selectionFilter (list; optional)
- showBorders (boolean; default False)
- showColumnHeaders (boolean; default True)
- showColumnLines (boolean; default True)
- showRowLines (boolean; default False)
- sortByGroupSummaryInfo (list of dicts; optional)
- sorting (dict; optional)
- stateStoring (dict; optional)
- summary (dict; optional)
- tabIndex (number; default 0)
- twoWayBindingEnabled (boolean; default True)
- visible (boolean; default True)
- width (number | string; optional)
- wordWrapEnabled (boolean; default False)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, allowColumnReordering=Component.UNDEFINED, allowColumnResizing=Component.UNDEFINED, cacheEnabled=Component.UNDEFINED, cellHintEnabled=Component.UNDEFINED, columnAutoWidth=Component.UNDEFINED, columnChooser=Component.UNDEFINED, columnFixing=Component.UNDEFINED, columnHidingEnabled=Component.UNDEFINED, columnMinWidth=Component.UNDEFINED, columnResizingMode=Component.UNDEFINED, columns=Component.UNDEFINED, columnWidth=Component.UNDEFINED, customizeColumns=Component.UNDEFINED, customizeExportData=Component.UNDEFINED, dataSource=Component.UNDEFINED, dateSerializationFormat=Component.UNDEFINED, disabled=Component.UNDEFINED, editing=Component.UNDEFINED, elementAttr=Component.UNDEFINED, errorRowEnabled=Component.UNDEFINED, export=Component.UNDEFINED, filterBuilder=Component.UNDEFINED, filterBuilderPopup=Component.UNDEFINED, filterPanel=Component.UNDEFINED, filterRow=Component.UNDEFINED, filterSyncEnabled=Component.UNDEFINED, filterValue=Component.UNDEFINED, focusedColumnIndex=Component.UNDEFINED, focusedRowEnabled=Component.UNDEFINED, focusedRowIndex=Component.UNDEFINED, focusedRowKey=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, grouping=Component.UNDEFINED, groupPanel=Component.UNDEFINED, headerFilter=Component.UNDEFINED, height=Component.UNDEFINED, highlightChanges=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, keyExpr=Component.UNDEFINED, loadPanel=Component.UNDEFINED, masterDetail=Component.UNDEFINED, noDataText=Component.UNDEFINED, onAdaptiveDetailRowPreparing=Component.UNDEFINED, onCellClick=Component.UNDEFINED, onCellHoverChanged=Component.UNDEFINED, onCellPrepared=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onContextMenuPreparing=Component.UNDEFINED, onDataErrorOccurred=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onEditingStart=Component.UNDEFINED, onEditorPrepared=Component.UNDEFINED, onEditorPreparing=Component.UNDEFINED, onExported=Component.UNDEFINED, onExporting=Component.UNDEFINED, onFileSaving=Component.UNDEFINED, onFocusedCellChanged=Component.UNDEFINED, onFocusedCellChanging=Component.UNDEFINED, onFocusedRowChanged=Component.UNDEFINED, onFocusedRowChanging=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onInitNewRow=Component.UNDEFINED, onKeyDown=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onRowClick=Component.UNDEFINED, onRowCollapsed=Component.UNDEFINED, onRowCollapsing=Component.UNDEFINED, onRowExpanded=Component.UNDEFINED, onRowExpanding=Component.UNDEFINED, onRowInserted=Component.UNDEFINED, onRowInserting=Component.UNDEFINED, onRowPrepared=Component.UNDEFINED, onRowRemoved=Component.UNDEFINED, onRowRemoving=Component.UNDEFINED, onRowUpdated=Component.UNDEFINED, onRowUpdating=Component.UNDEFINED, onRowValidating=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, onToolbarPreparing=Component.UNDEFINED, pager=Component.UNDEFINED, paging=Component.UNDEFINED, remoteOperations=Component.UNDEFINED, renderAsync=Component.UNDEFINED, repaintChangesOnly=Component.UNDEFINED, rowAlternationEnabled=Component.UNDEFINED, rowTemplate=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scrolling=Component.UNDEFINED, searchPanel=Component.UNDEFINED, selectedRowKeys=Component.UNDEFINED, selection=Component.UNDEFINED, selectionFilter=Component.UNDEFINED, showBorders=Component.UNDEFINED, showColumnHeaders=Component.UNDEFINED, showColumnLines=Component.UNDEFINED, showRowLines=Component.UNDEFINED, sortByGroupSummaryInfo=Component.UNDEFINED, sorting=Component.UNDEFINED, stateStoring=Component.UNDEFINED, summary=Component.UNDEFINED, tabIndex=Component.UNDEFINED, twoWayBindingEnabled=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, wordWrapEnabled=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'allowColumnReordering', 'allowColumnResizing', 'cacheEnabled', 'cellHintEnabled', 'columnAutoWidth', 'columnChooser', 'columnFixing', 'columnHidingEnabled', 'columnMinWidth', 'columnResizingMode', 'columns', 'columnWidth', 'dataSource', 'dateSerializationFormat', 'disabled', 'editing', 'elementAttr', 'errorRowEnabled', 'export', 'filterBuilder', 'filterBuilderPopup', 'filterPanel', 'filterRow', 'filterSyncEnabled', 'filterValue', 'focusedColumnIndex', 'focusedRowEnabled', 'focusedRowIndex', 'focusedRowKey', 'focusStateEnabled', 'grouping', 'groupPanel', 'headerFilter', 'height', 'highlightChanges', 'hint', 'hoverStateEnabled', 'keyExpr', 'loadPanel', 'masterDetail', 'noDataText', 'onCellClick', 'onRowClick', 'pager', 'paging', 'remoteOperations', 'renderAsync', 'repaintChangesOnly', 'rowAlternationEnabled', 'rowTemplate', 'rtlEnabled', 'scrolling', 'searchPanel', 'selectedRowKeys', 'selection', 'selectionFilter', 'showBorders', 'showColumnHeaders', 'showColumnLines', 'showRowLines', 'sortByGroupSummaryInfo', 'sorting', 'stateStoring', 'summary', 'tabIndex', 'twoWayBindingEnabled', 'visible', 'width', 'wordWrapEnabled']
        self._type = 'DataGrid'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'allowColumnReordering', 'allowColumnResizing', 'cacheEnabled', 'cellHintEnabled', 'columnAutoWidth', 'columnChooser', 'columnFixing', 'columnHidingEnabled', 'columnMinWidth', 'columnResizingMode', 'columns', 'columnWidth', 'dataSource', 'dateSerializationFormat', 'disabled', 'editing', 'elementAttr', 'errorRowEnabled', 'export', 'filterBuilder', 'filterBuilderPopup', 'filterPanel', 'filterRow', 'filterSyncEnabled', 'filterValue', 'focusedColumnIndex', 'focusedRowEnabled', 'focusedRowIndex', 'focusedRowKey', 'focusStateEnabled', 'grouping', 'groupPanel', 'headerFilter', 'height', 'highlightChanges', 'hint', 'hoverStateEnabled', 'keyExpr', 'loadPanel', 'masterDetail', 'noDataText', 'onCellClick', 'onRowClick', 'pager', 'paging', 'remoteOperations', 'renderAsync', 'repaintChangesOnly', 'rowAlternationEnabled', 'rowTemplate', 'rtlEnabled', 'scrolling', 'searchPanel', 'selectedRowKeys', 'selection', 'selectionFilter', 'showBorders', 'showColumnHeaders', 'showColumnLines', 'showRowLines', 'sortByGroupSummaryInfo', 'sorting', 'stateStoring', 'summary', 'tabIndex', 'twoWayBindingEnabled', 'visible', 'width', 'wordWrapEnabled']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DataGrid, self).__init__(**args)
