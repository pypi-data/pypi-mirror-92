from abc import ABC, abstractmethod
from types import SimpleNamespace
from collections import namedtuple

import streamlit_elements.core.utils as utils
from streamlit_elements.core.base import ReactBase, render_component
from streamlit_elements.core.element import ReactElement


class ReactContext(ReactBase):
    """React context class."""
    __slots__ = ("_code", "_modules", "_document", "_element_stack", "_default_state", "_default_storage")

    def __init__(self):
        self._code = None
        self._modules = []
        self._document = []
        self._element_stack = [ElementStack("root")]
        self._default_state = {}
        self._default_storage = {}

    def _serialize(self):
        # Build context representation if it doesn't exist yet
        if self._code is None:
            self._resolve_context()
            self._code = utils.serialize(self._document)
        
        return self._code

    def _register_module(self, module):
        self._modules.append(module)
    
    def _register_element(self, element):
        self._code = None  # Invalidate previous code

        stack = self._element_stack[-1]
        stack.pending_children.append(element)

        if element._parent is None:
            element._parent = stack.default_parent
    
    def _push_context(self, parent):
        self._element_stack.append(ElementStack(parent))
    
    def _pop_context(self):
        self._resolve_context()
        del self._element_stack[-1]

    def _resolve_context(self):
        stack = self._element_stack[-1]

        for child in stack.pending_children:
            if child._parent is not None:
                if isinstance(child._parent, ReactElement):
                    child._parent(child)
                elif child._parent == "root":
                    self._document.append(child)

                child._parent = None
        
        stack.pending_children.clear()
    
    def default_state(self, **defaults):
        self._default_state = defaults

    def default_storage(self, **defaults):
        self._default_storage = defaults
    
    def show(self, key=None, clear=True):
        """Render a component.
        
        Parameters
        ----------
        key : str or None
            An optional string to use as the unique key for the widget.
            If this is omitted, a key will be generated for the widget
            based on its content. Multiple widgets of the same type may
            not share the same key.
        clear : boolean
        """
        result = render_component(
            code=self._serialize(),
            modules=self._modules,
            defaultState=self._default_state,
            defaultStorage=self._default_storage,
            key=key,
            default={
                "state": self._default_state.copy(),
                "storage": self._default_storage.copy(),
            }
        )

        if clear:
            self._document.clear()
            self._default_state.clear()
            self._default_storage.clear()

        return ReactResult(result)


class ElementStack:
    """Element stack entry."""
    __slots__ = ("default_parent", "pending_children")

    def __init__(self, default_parent):
        self.default_parent = default_parent
        self.pending_children = []


class ReactResult:
    """Result object of context show."""
    __slots__ = ("state", "storage")

    def __init__(self, result):
        if result is not None:
            self.state = ReactData(**result.get("state", {}))
            self.storage = ReactData(**result.get("storage", {}))
        else:
            self.state = ReactData()
            self.storage = ReactData()


class ReactData(SimpleNamespace):
    """A class to store result with a safe attribute getter."""

    def __getattr__(self, attr):
        """Called when attribute does not exist."""
        return None
