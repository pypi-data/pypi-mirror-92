import streamlit_elements.core.utils as utils
from streamlit_elements.core.base import ReactBase


class ReactStatement(ReactBase):
    """React statement."""
    __slots__ = "_stmt"

    def __init__(self, stmt):
        self._stmt = stmt

    def _serialize(self):
        return self._stmt

    def __pos__(self):
        return ReactStatement(f"(+{self._stmt})")
    
    def __neg__(self):
        return ReactStatement(f"(-{self._stmt})")

    def __invert__(self):
        return ReactStatement(f"(!{self._stmt})")
    
    def __and__(self, value):
        return ReactStatement(f"({self._stmt}&&{utils.serialize(value)})")

    def __or__(self, value):
        return ReactStatement(f"({self._stmt}||{utils.serialize(value)})")
    
    def __eq__(self, value):
        return ReactStatement(f"(eq({self._stmt},{utils.serialize(value)}))")

    def __ne__(self, value):
        return ReactStatement(f"(!eq({self._stmt},{utils.serialize(value)}))")

    def __ge__(self, value):
        return ReactStatement(f"({self._stmt}>={utils.serialize(value)})")

    def __gt__(self, value):
        return ReactStatement(f"({self._stmt}>{utils.serialize(value)})")

    def __le__(self, value):
        return ReactStatement(f"({self._stmt}<={utils.serialize(value)})")

    def __lt__(self, value):
        return ReactStatement(f"({self._stmt}<{utils.serialize(value)})")

    def __add__(self, value):
        return ReactStatement(f"({self._stmt}+{utils.serialize(value)})")

    def __sub__(self, value):
        return ReactStatement(f"({self._stmt}-{utils.serialize(value)})")

    def __mul__(self, value):
        return ReactStatement(f"({self._stmt}*{utils.serialize(value)})")

    def __div__(self, value):
        return ReactStatement(f"({self._stmt}/{utils.serialize(value)})")

    def __radd__(self, value):
        return ReactStatement(f"({utils.serialize(value)}+{self._stmt})")

    def __rsub__(self, value):
        return ReactStatement(f"({utils.serialize(value)}-{self._stmt})")

    def __rmul__(self, value):
        return ReactStatement(f"({utils.serialize(value)}*{self._stmt})")

    def __rdiv__(self, value):
        return ReactStatement(f"({utils.serialize(value)}/{self._stmt})")

    def __getitem__(self, child):
        return ReactStatement(f"{self._stmt}[{utils.serialize(child)}]")

    def __getattr__(self, child):
        return ReactStatement(f"{self._stmt}[{utils.serialize(child)}]")
    
    def __call__(self, *args):
        return ReactStatement(f"{self._stmt}({','.join(utils.serialize(arg) for arg in args)})")
