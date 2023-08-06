import streamlit_elements.core.utils as utils
from streamlit_elements.core.module import ReactModuleDynamic


class Svg(ReactModuleDynamic):
    """Svg elements."""
    __slots__ = ()

    def _element_case(self, name):
        return utils.to_camel_case(name)
