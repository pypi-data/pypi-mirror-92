from collections.abc import Generator

import streamlit_elements.core.utils as utils
from streamlit_elements.core.base import ReactBase


class ReactElement(ReactBase):
    """A react node."""
    __slots__ = ("_element", "_props", "_children", "_module", "_parent")

    def __init__(self, element, module, parent=None, element_case=None):
        self._props = []
        self._children = []
        self._module = module
        self._parent = parent

        if element_case:
            self._element = element_case(element)
        else:
            self._element = module._element_case(element)

        self._module._register_element(self)

    def _serialize(self):
        props = ",".join(self._props)
        children = ",".join(self._children)
        module_name = utils.to_json(self._module._name)

        return f"create({module_name},{self._element},{{{props}}},[{children}])"

    def __enter__(self):
        self._module._push_context(self)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._module._pop_context()

    def __getattr__(self, element):
        return ReactElement(element, self._module, self)

    def __getitem__(self, element):
        return ReactElement(element, self._module, self, utils.to_json)
    
    def __call__(self, children=None, **props):
        if props:
            self._props.append(",".join(
                utils.to_camel_case(prop) + ":" + utils.serialize(value)
                for prop, value in props.items()
            ))

        if children is not None:
            if isinstance(children, (list, tuple, set, Generator)):
                self._children.append(",".join(utils.serialize(child) for child in children))
            else:
                self._children.append(utils.serialize(children))

        return self
