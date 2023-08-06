from streamlit_elements.core.module import ReactModuleFixed


class MonacoEditor(ReactModuleFixed):
    """Monaco editor (https://github.com/react-monaco-editor/react-monaco-editor)"""
    __slots__ = ()

    def editor(self, **props):
        self._create_element("MonacoEditor", **props)

    def diff(self, **props):
        self._create_element("DiffEditor", **props)
