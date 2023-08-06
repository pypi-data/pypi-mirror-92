from streamlit_elements.core.context import ReactContext as _ReactContext
from streamlit_elements.version import __version__

from streamlit_elements.modules.charts.nivo import Nivo as _Nivo
from streamlit_elements.modules.charts.recharts import Recharts as _Recharts
from streamlit_elements.modules.core.events import Events as _Events
from streamlit_elements.modules.core.html import Html as _Html
from streamlit_elements.modules.core.objects import Objects as _Objects
from streamlit_elements.modules.core.svg import Svg as _Svg
from streamlit_elements.modules.editors.monaco import MonacoEditor as _MonacoEditor
from streamlit_elements.modules.editors.quill import QuillEditor as _QuillEditor
from streamlit_elements.modules.material.elements import MaterialElements as _MaterialElements
from streamlit_elements.modules.material.icons import MaterialIcons as _MaterialIcons
from streamlit_elements.modules.media.player import Player as _Player
from streamlit_elements.modules.social.facebook import Facebook as _Facebook
from streamlit_elements.modules.social.instagram import Instagram as _Instagram
from streamlit_elements.modules.social.twitter import Twitter as _Twitter


class Elements(_ReactContext):

    def __init__(self):
        super().__init__()

        # Core
        self.html = _Html(self)
        self.svg = _Svg(self)
        self.events = _Events(self)
        self.objects = _Objects(self)

        # Material
        self.material = _MaterialElements(self)
        self.icons = _MaterialIcons(self)

        # Charts
        self.nivo = _Nivo(self)
        self.recharts = _Recharts(self)

        # Editors
        self.monaco = _MonacoEditor(self)
        self.quill = _QuillEditor(self)

        # Media
        self.player = _Player(self)

        # Social
        self.facebook = _Facebook(self)
        self.instagram = _Instagram(self)
        self.twitter = _Twitter(self)
    
    def __getattr__(self, attr):
        if hasattr(self.objects, attr):
            return getattr(self.objects, attr)
        elif hasattr(self.events, attr):
            return getattr(self.events, attr)
        else:
            return getattr(self.material, attr)
        
    def __getitem__(self, item):
        return getattr(self, item)


class _Element:

    def _get_element(self, element):
        def _show_element(*args, key=None, **kwargs):
            elements = Elements()
            elements[element](*args, **kwargs)
            return elements.show(key)
        return _show_element
    
    __getattr__ = _get_element
    __getitem__ = _get_element


element = _Element()
