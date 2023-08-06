import streamlit_elements.core.utils as utils
from streamlit_elements.core.module import ReactModuleDynamic


class Html(ReactModuleDynamic):
    """HTML elements."""
    __slots__ = ()

    def _element_case(self, name):
        return utils.to_lower_case(name)
