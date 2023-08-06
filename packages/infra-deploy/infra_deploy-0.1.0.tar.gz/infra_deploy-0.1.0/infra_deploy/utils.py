from contextlib import suppress
from typing import List, TYPE_CHECKING, Any, Dict, Optional, Tuple, Type, Union

import pytest
from decorator import contextmanager
from loguru import logger
import pybase64

from infra_deploy.models.labels import DictAny

BAE = Type[BaseException]


@contextmanager
def soft_raises(expected_exception: Optional[Union[BAE, Tuple[BAE, ...]]]):
    if expected_exception is None:
        yield
        return

    with pytest.raises(expected_exception):
        yield


def in_ipython() -> bool:
    """
    Check whether we're in an ipython environment, including jupyter notebooks.
    """
    try:
        eval('__IPYTHON__')
    except NameError:
        return False
    else:    # pragma: no cover
        return True


def remove_nones_dict(original: dict):
    if isinstance(original, dict):
        return {
            k: v
            for k,
            v in ((k,
                   remove_nones_dict(v)) for k,
                  v in original.items())
            if v
        }
    if isinstance(original, list):
        return [v for v in map(remove_nones_dict, original) if v]
    return original


def update_not_none(mapping: Dict[Any, Any], **update: Any) -> None:
    mapping.update({k: v for k, v in update.items() if v is not None})


def kill_none(mapping: Dict[Any, Any], **update: Any) -> None:
    update_not_none(mapping, **update)


def pull_kube(item: Any) -> Optional[Any]:
    is_supressed: bool = False

    if hasattr(item, "to_kube"):
        with suppress(Exception):
            is_supressed = True
            return item.to_kube()
    # Will return a none that should be filtered
    if is_supressed:
        return None

    return item


def rip_meta(_metadata: DictAny) -> DictAny:
    """Extracts metadata fields. Removes duds if they exist.

    Args:
        _metadata (DictAny): The local metadata for the Entity system.

    Returns:
        DictAny: The pulled apart metadata.
    """
    converted_kube = {k: pull_kube(v) for k, v in _metadata.items()}
    remove_nones_dict(converted_kube)
    return converted_kube


def b64_ls(arr: List[str]) -> str:
    """Take a list of strings and create a consistent base64 of it. Returns "" if it's empty.

    Args:
        arr (List[str]): List of strings

    Returns:
        str: encoded string
    """
    if not arr:
        return ""
    sorted_agg_str: List[str] = sorted(arr)
    joined_agg_str = ":".join(sorted_agg_str)
    return pybase64.b64encode_as_string(str.encode(joined_agg_str))


# trick PyRight into thinking that it might be both False or True
RUNTIME = not TYPE_CHECKING

if RUNTIME:

    def autocomplete(model):
        return model
else:
    from dataclasses import dataclass as autocomplete


def map_fields(init_dict, map_dict, res_dict=None):
    logger.info("Starting map conversion")
    logger.warning(map_dict)
    logger.debug(init_dict)
    if not hasattr(map_dict, "keys"):
        return init_dict
    res_dict = res_dict or {}
    for k, v in init_dict.items():
        # print("Key: ", k)
        if isinstance(v, dict):
            # print("value is a dict - recursing")
            v = map_fields(v, map_dict[k])
        elif k in map_dict.keys():
            # print("Remapping:", k, str(map_dict[k]))
            k = str(map_dict[k])
        res_dict[k] = v
    return res_dict