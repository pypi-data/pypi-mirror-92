from streamlit_elements.core.module import ReactModuleFixed


class QuillEditor(ReactModuleFixed):
    """Quill Editor.

    Quill is a modern rich text editor built for compatibility and extensibility.

    Documentation
    -------------
    https://github.com/zenoamaro/react-quill

    """
    __slots__ = ()

    def __call__(self, **props):
        """Create a new quill editor.

        Parameters
        ----------
        props : list
            Quill component properties.
            Only one theme is supported (snow).
        
        """
        self._create_element("QuillEditor", **props)
