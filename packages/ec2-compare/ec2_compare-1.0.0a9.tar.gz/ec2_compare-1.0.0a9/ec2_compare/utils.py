"""
Utils module.
"""
from typing import Dict, List, Any
import collections.abc


def module_name(search_key: str):
    """Returns the module name from search key"""

    return "".join([
        ("_" + i if j > 0 and i.isupper() else i) for j, i in enumerate(
            search_key.replace("Supported", "").replace("Types", "").replace(
                "-", "_"))
    ]).strip().lower()


def dict_values(data: Dict, keys: List[Any],
                default: List[Any] = None,
                limit: int = None):
    """Generator returns values for list of keys from dictionary"""
    cntr = 0
    if isinstance(keys, set):
        keys = list(keys)

    for key in keys:
        if not isinstance(key, collections.abc.Hashable):
            continue
        _val = data.get(key, None)
        if _val is None:
            continue
        yield _val
        cntr += 1
        if limit is not None and cntr >= limit:
            break

    if isinstance(default, set):
        default = list(default)
    elif default is None:
        return
    elif not isinstance(default, list):
        default = [default]

    for _val in default:
        if not isinstance(_val, collections.abc.Hashable):
            continue
        if limit is not None and cntr >= limit:
            break
        yield _val
        cntr += 1
