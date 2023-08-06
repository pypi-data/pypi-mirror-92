# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TabPanel(Component):
    """A TabPanel component.


Keyword arguments:
- id (string; optional): The ID used to identify this compnent in Dash callbacks
- accessKey (string; optional)
- activeStateEnabled (boolean; default False)
- animationEnabled (boolean; default True)
- dataSource (string | list of strings | list of dicts | dict; optional)
- deferRendering (boolean; default True)
- disabled (boolean; default False)
- elementAttr (dict; optional)
- focusStateEnabled (boolean; default False)
- height (number | string; default 'auto')
- hint (string; optional)
- hoverStateEnabled (boolean; default True)
- itemHoldTimeout (number; default 750)
- items (list of strings | list of dicts; default undefined)
- itemTemplate (string | dict; default 'item')
- itemTitleTemplate (string | dict; default 'title')
- loop (boolean; default False)
- noDataText (string; default 'No data to display')
- onItemClick (string; optional)
- onTitleClick (string; optional)
- repaintChangesOnly (boolean; default False)
- rtlEnabled (boolean; default False)
- scrollByContent (boolean; default True)
- scrollingEnabled (boolean; default True)
- selectedIndex (number; default 0)
- selectedItem (dict; optional)
- showNavButtons (boolean; default False)
- swipeEnabled (boolean; default True)
- tabIndex (number; default 0)
- visible (boolean; default True)
- width (number | string; default 'auto')"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, animationEnabled=Component.UNDEFINED, dataSource=Component.UNDEFINED, deferRendering=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, itemHoldTimeout=Component.UNDEFINED, items=Component.UNDEFINED, itemComponent=Component.UNDEFINED, itemTemplate=Component.UNDEFINED, itemTitleRender=Component.UNDEFINED, itemTitleTemplate=Component.UNDEFINED, loop=Component.UNDEFINED, noDataText=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onItemClick=Component.UNDEFINED, onItemContextMenu=Component.UNDEFINED, onItemHold=Component.UNDEFINED, onItemRendered=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, onTitleClick=Component.UNDEFINED, onTitleHold=Component.UNDEFINED, onTitleRendered=Component.UNDEFINED, repaintChangesOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scrollByContent=Component.UNDEFINED, scrollingEnabled=Component.UNDEFINED, selectedIndex=Component.UNDEFINED, selectedItem=Component.UNDEFINED, showNavButtons=Component.UNDEFINED, swipeEnabled=Component.UNDEFINED, tabIndex=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'animationEnabled', 'dataSource', 'deferRendering', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'itemHoldTimeout', 'items', 'itemTemplate', 'itemTitleTemplate', 'loop', 'noDataText', 'onItemClick', 'onTitleClick', 'repaintChangesOnly', 'rtlEnabled', 'scrollByContent', 'scrollingEnabled', 'selectedIndex', 'selectedItem', 'showNavButtons', 'swipeEnabled', 'tabIndex', 'visible', 'width']
        self._type = 'TabPanel'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'animationEnabled', 'dataSource', 'deferRendering', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'itemHoldTimeout', 'items', 'itemTemplate', 'itemTitleTemplate', 'loop', 'noDataText', 'onItemClick', 'onTitleClick', 'repaintChangesOnly', 'rtlEnabled', 'scrollByContent', 'scrollingEnabled', 'selectedIndex', 'selectedItem', 'showNavButtons', 'swipeEnabled', 'tabIndex', 'visible', 'width']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TabPanel, self).__init__(**args)
