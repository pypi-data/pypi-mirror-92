from streamlit_elements.core.module import ReactModuleFixed


class Player(ReactModuleFixed):
    """React player element."""
    __slots__ = ()

    def __call__(self, **props):
        self._create_element("ReactPlayer", **props)
