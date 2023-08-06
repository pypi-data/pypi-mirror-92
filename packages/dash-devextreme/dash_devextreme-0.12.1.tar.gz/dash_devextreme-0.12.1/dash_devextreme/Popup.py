# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Popup(Component):
    """A Popup component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional)
- id (string; optional): The ID used to identify this compnent in Dash callbacks
- accessKey (string; optional): Specifies the shortcut key that sets focus on the UI component
- animation (dict; optional)
- closeOnOutsideClick (boolean; optional)
- container (string; optional)
- deferRendering (boolean; optional)
- disabled (boolean; optional)
- dragEnabled (boolean; optional)
- elementAttr (dict; optional)
- focusStateEnabled (boolean; optional)
- fullScreen (boolean; optional)
- height (number | string; optional)
- hint (string; optional)
- hoverStateEnabled (boolean; optional)
- maxHeight (number | string; optional)
- maxWidth (number | string; optional)
- minHeight (number | string; optional)
- minWidth (number | string; optional)
- position (a value equal to: 'bottom' | 'center' | 'left' | 'left bottom' | 'left top' | 'right' | 'right bottom' | 'right top' | 'top' | dict; optional)
- resizeEnabled (boolean; optional)
- rtlEnabled (boolean; optional)
- shading (boolean; optional)
- shadingColor (string; optional)
- showCloseButton (boolean; optional)
- showTitle (boolean; optional)
- tabIndex (number; optional)
- title (string; optional)
- titleTemplate (string; optional)
- toolbarItems (list of dicts; optional)
- visible (boolean; optional)
- width (number | string; optional)
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, animation=Component.UNDEFINED, closeOnOutsideClick=Component.UNDEFINED, container=Component.UNDEFINED, deferRendering=Component.UNDEFINED, disabled=Component.UNDEFINED, dragEnabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, fullScreen=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, maxHeight=Component.UNDEFINED, maxWidth=Component.UNDEFINED, minHeight=Component.UNDEFINED, minWidth=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onHidden=Component.UNDEFINED, onHiding=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onResize=Component.UNDEFINED, onResizeEnd=Component.UNDEFINED, onResizeStart=Component.UNDEFINED, onShowing=Component.UNDEFINED, onShown=Component.UNDEFINED, position=Component.UNDEFINED, resizeEnabled=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, shading=Component.UNDEFINED, shadingColor=Component.UNDEFINED, showCloseButton=Component.UNDEFINED, showTitle=Component.UNDEFINED, tabIndex=Component.UNDEFINED, title=Component.UNDEFINED, titleTemplate=Component.UNDEFINED, toolbarItems=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'accessKey', 'animation', 'closeOnOutsideClick', 'container', 'deferRendering', 'disabled', 'dragEnabled', 'elementAttr', 'focusStateEnabled', 'fullScreen', 'height', 'hint', 'hoverStateEnabled', 'maxHeight', 'maxWidth', 'minHeight', 'minWidth', 'position', 'resizeEnabled', 'rtlEnabled', 'shading', 'shadingColor', 'showCloseButton', 'showTitle', 'tabIndex', 'title', 'titleTemplate', 'toolbarItems', 'visible', 'width', 'loading_state']
        self._type = 'Popup'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'accessKey', 'animation', 'closeOnOutsideClick', 'container', 'deferRendering', 'disabled', 'dragEnabled', 'elementAttr', 'focusStateEnabled', 'fullScreen', 'height', 'hint', 'hoverStateEnabled', 'maxHeight', 'maxWidth', 'minHeight', 'minWidth', 'position', 'resizeEnabled', 'rtlEnabled', 'shading', 'shadingColor', 'showCloseButton', 'showTitle', 'tabIndex', 'title', 'titleTemplate', 'toolbarItems', 'visible', 'width', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Popup, self).__init__(children=children, **args)
