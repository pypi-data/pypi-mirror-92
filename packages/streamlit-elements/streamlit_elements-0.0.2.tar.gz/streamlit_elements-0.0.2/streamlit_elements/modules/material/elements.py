from streamlit_elements.core.module import ReactModuleDynamic


class MaterialElements(ReactModuleDynamic):
    """Material UI elements (https://material-ui.com/)."""
    __slots__ = ()

    @property
    def markdown(self):
        return self._create_element("GfmMarkdown")
    
    @property
    def qrcode(self):
        return self._create_element("QRCode")
