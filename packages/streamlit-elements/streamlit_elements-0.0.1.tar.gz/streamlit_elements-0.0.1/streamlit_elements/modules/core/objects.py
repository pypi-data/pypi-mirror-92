from streamlit_elements.core.module import ReactModuleFixed
from streamlit_elements.core.state import ReactState
from streamlit_elements.core.statement import ReactStatement


class Objects(ReactModuleFixed):
    """Event elements."""
    __slots__ = ()

    @property
    def state(self):
        return ReactState("state", "setState")
    
    @property
    def storage(self):
        return ReactState("storage", "setStorage")

    @property
    def console(self):
        return ReactStatement("console")

    @property
    def submit(self):
        return ReactStatement("submit")
    
    @property
    def rerun(self):
        """Alias for submit."""
        return ReactStatement("submit")
