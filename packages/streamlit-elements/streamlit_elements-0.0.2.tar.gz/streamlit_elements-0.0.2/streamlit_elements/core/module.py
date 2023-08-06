from abc import ABC

import streamlit_elements.core.utils as utils
from streamlit_elements.core.element import ReactElement


class ReactModuleBase(ABC):
    """React module."""
    __slots__ = ("_context", "_name", "_registered")

    def __init__(self, context):
        self._context = context
        self._name = self.__class__.__name__
        self._registered = False
    
    def _create_element(self, element, children=None, **props):
        element = ReactElement(element, self, element_case=utils.to_json)

        if props or children is not None:
            return element(children, **props)
        else:
            return element
    
    def _register_element(self, element):
        if not self._registered:
            self._context._register_module(self._name)
            self._registered = True

        self._context._register_element(element)
    
    def _push_context(self, parent):
        self._context._push_context(parent)
    
    def _pop_context(self):
        self._context._pop_context()

    def _element_case(self, name):
        return utils.to_pascal_case(name)


class ReactModuleFixed(ReactModuleBase):
    """React module with fixed elements."""
    __slots__ = ()


class ReactModuleDynamic(ReactModuleBase):
    """React module with dynamic elements."""
    __slots__ = ()

    def __getattr__(self, element):
        return ReactElement(element, self)

    def __getitem__(self, element):
        return ReactElement(element, self, element_case=utils.to_json)
