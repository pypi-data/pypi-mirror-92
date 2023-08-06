import json
import types
from collections.abc import Mapping, Generator

from streamlit_elements.core.base import ReactBase
from streamlit_elements.core.callback import ReactCallback
from streamlit_elements.core.element import ReactElement


def serialize(obj):
    """Handle object serialization for ReactBase subclasses, lambdas and regular data types."""
    if isinstance(obj, ReactElement):
        obj._parent = None
        return obj._serialize()

    elif isinstance(obj, ReactBase):
        return obj._serialize()

    elif isinstance(obj, types.LambdaType) and obj.__name__ == "<lambda>":
        return ReactCallback(obj)._serialize()

    elif isinstance(obj, Mapping):
        return "{" + ",".join(to_json(key) + ":" + serialize(val) for key, val in obj.items()) + "}"

    elif isinstance(obj, (list, tuple, set, Generator)):
        return "[" + ",".join(map(serialize, obj)) + "]"

    return to_json(obj)


def to_json(obj):
    return json.dumps(obj, separators=(",", ":"), check_circular=False)


def to_camel_case(string):
    """Convert a string from snake_case to camelCase."""
    return to_json(string[0] + string.title().replace("_", "")[1:])


def to_pascal_case(string):
    """Convert a string from snake_case to PascalCase."""
    return to_json(string.title().replace("_", ""))


def to_lower_case(string):
    """Convert a string from snake_case to lowercase."""
    return to_json(string.replace("_", "").lower())
