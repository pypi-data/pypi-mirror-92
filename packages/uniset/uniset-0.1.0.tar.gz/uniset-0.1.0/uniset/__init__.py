from uniset._category import MAINCATEGORIES, SUBCATEGORIES

__all__ = SUBCATEGORIES + MAINCATEGORIES + ("WHITESPACE", "PUNCTUATION")
__version__ = "0.1.0"

import importlib
import string
import sys
from typing import FrozenSet

_THIS_MODULE = sys.modules[__name__]


def __getattr__(name: str) -> FrozenSet[str]:
    """Attribute getter fallback.

    We use `__getattr__` instead of importing all frozensets directly in
    this module to achieve lazy loading, i.e. calling `import uniset`
    will not load any of the sets into memory.
    """
    if name in SUBCATEGORIES:
        char_set = _get_subcategory_set(name)
    elif name in MAINCATEGORIES:
        char_set = _get_maincategory_set(name)
    elif name == "WHITESPACE":
        char_set = frozenset(string.whitespace) | _get_subcategory_set("Zs")
    elif name == "PUNCTUATION":
        char_set = frozenset(string.punctuation) | _get_maincategory_set("P")
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    # Cache the value in this module for next time, so that `__getattr__`
    # is only called once per `name`.
    setattr(_THIS_MODULE, name, char_set)
    return char_set


def _get_subcategory_set(subcategory: str) -> FrozenSet[str]:
    subcategory_module = importlib.import_module(
        "._category." + subcategory.lower(), __name__
    )
    return getattr(subcategory_module, subcategory)


def _get_maincategory_set(category: str) -> FrozenSet[str]:
    subcategories = {c for c in SUBCATEGORIES if c.startswith(category)}
    char_set: FrozenSet[str] = frozenset()
    for subcategory in subcategories:
        char_set |= _get_subcategory_set(subcategory)
    return char_set
