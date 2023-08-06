import streamlit_elements.core.utils as utils
from streamlit_elements.core.statement import ReactStatement


class ReactState:
    """React state object."""
    __slots__ = ("_type", "_setter")

    def __init__(self, type, setter):
        self._type = type
        self._setter = setter
    
    def __getattr__(self, child):
        return ReactStateObject(self._type, self._setter, utils.serialize(child))


class ReactStateObject(ReactStatement):
    """React object with additional methods state specific."""
    __slots__ = ("_setter", "_child")

    def __init__(self, type, setter, child):
        super().__init__(f"{type}[{child}]")
        self._setter = setter
        self._child = child
    
    def set(self, value):
        return ReactStatement(f"{self._setter}(prev=>({{...prev,{self._child}:{utils.serialize(value)}}}))")
