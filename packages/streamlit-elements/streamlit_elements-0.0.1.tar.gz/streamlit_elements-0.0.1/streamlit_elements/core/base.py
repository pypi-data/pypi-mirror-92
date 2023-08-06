from abc import ABC, abstractmethod
from pathlib import Path
from streamlit.components.v1 import declare_component
from streamlit_elements import version


if version.__release__:
    _source = {"path": (Path(version.__file__).parent/"frontend"/"build").resolve()}
else:
    _source = {"url": "http://localhost:3001"}

render_component = declare_component("streamlit_elements", **_source)


class ReactBase(ABC):
    """A serializable react object."""
    __slots__ = ()

    @abstractmethod
    def _serialize(self):
        pass
