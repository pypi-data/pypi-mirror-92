from streamlit_elements.core.module import ReactModuleFixed
from streamlit_elements.core.statement import ReactStatement


class Events(ReactModuleFixed):
    """Event elements."""
    __slots__ = ()

    def on_load(self, callback):
        self._create_element("EventLoad", callback=callback)

    def on_update(self, callback):
        self._create_element("EventUpdate", code=ReactStatement("code"), callback=callback)
        
    def on_change(self, callback):
        self._create_element("EventChange", callback=callback)

    def on_interval(self, seconds, callback):
        self._create_element("EventInterval", seconds=seconds, callback=callback)

    def on_hotkey(self, sequence, callback, override=False):
        self._create_element("EventHotkey", sequence=sequence, callback=callback, override=override)
