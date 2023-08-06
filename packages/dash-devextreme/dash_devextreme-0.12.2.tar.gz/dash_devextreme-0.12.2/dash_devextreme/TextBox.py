# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TextBox(Component):
    """A TextBox component.


Keyword arguments:
- id (string; optional): The ID used to identify this compnent in Dash callbacks
- accessKey (string; optional)
- activeStateEnabled (boolean; default False)
- disabled (boolean; default False)
- elementAttr (dict; optional)
- focusStateEnabled (boolean; default True)
- height (number | string; default undefined)
- hint (string; default undefined)
- hoverStateEnabled (boolean; default True)
- inputAttr (dict; optional)
- isValid (boolean; default True)
- mask (string; default '')
- maskChar (string; default '_')
- maskInvalidMessage (string; default 'Value is invalid')
- maskRules (dict; optional)
- maxLength (string | number; optional)
- mode (a value equal to: 'email', 'password', 'search', 'tel', 'text', 'url'; default 'text')
- name (string; default '')
- placeholder (string; default '')
- readOnly (boolean; default False)
- rtlEnabled (boolean; default False)
- showClearButton (boolean; default False)
- showMaskMode (a value equal to: 'always', 'onFocus'; default 'always')
- spellcheck (boolean; default False)
- stylingMode (a value equal to: 'outlined', 'underlined', 'filled'; default 'outlined')
- tabIndex (number; default 0)
- useMaskedValue (boolean; default False)
- validationError (dict; default undefined)
- validationMessageMode (a value equal to: 'always', 'auto'; default 'auto')
- value (string; default '')
- valueChangeEvent (string; default 'change')
- visible (boolean; default True)
- width (number | string; default undefined)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, inputAttr=Component.UNDEFINED, isValid=Component.UNDEFINED, mask=Component.UNDEFINED, maskChar=Component.UNDEFINED, maskInvalidMessage=Component.UNDEFINED, maskRules=Component.UNDEFINED, maxLength=Component.UNDEFINED, mode=Component.UNDEFINED, name=Component.UNDEFINED, onChange=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onCopy=Component.UNDEFINED, onCut=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onEnterKey=Component.UNDEFINED, onFocusIn=Component.UNDEFINED, onFocusOut=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onInput=Component.UNDEFINED, onKeyDown=Component.UNDEFINED, onKeyPress=Component.UNDEFINED, onKeyUp=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onPaste=Component.UNDEFINED, onValueChanged=Component.UNDEFINED, placeholder=Component.UNDEFINED, readOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, showClearButton=Component.UNDEFINED, showMaskMode=Component.UNDEFINED, spellcheck=Component.UNDEFINED, stylingMode=Component.UNDEFINED, tabIndex=Component.UNDEFINED, useMaskedValue=Component.UNDEFINED, validationError=Component.UNDEFINED, validationMessageMode=Component.UNDEFINED, value=Component.UNDEFINED, valueChangeEvent=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'isValid', 'mask', 'maskChar', 'maskInvalidMessage', 'maskRules', 'maxLength', 'mode', 'name', 'placeholder', 'readOnly', 'rtlEnabled', 'showClearButton', 'showMaskMode', 'spellcheck', 'stylingMode', 'tabIndex', 'useMaskedValue', 'validationError', 'validationMessageMode', 'value', 'valueChangeEvent', 'visible', 'width']
        self._type = 'TextBox'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'isValid', 'mask', 'maskChar', 'maskInvalidMessage', 'maskRules', 'maxLength', 'mode', 'name', 'placeholder', 'readOnly', 'rtlEnabled', 'showClearButton', 'showMaskMode', 'spellcheck', 'stylingMode', 'tabIndex', 'useMaskedValue', 'validationError', 'validationMessageMode', 'value', 'valueChangeEvent', 'visible', 'width']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TextBox, self).__init__(**args)
