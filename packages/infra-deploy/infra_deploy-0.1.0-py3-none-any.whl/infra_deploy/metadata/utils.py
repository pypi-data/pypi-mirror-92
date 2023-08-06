from contextlib import suppress
from copy import deepcopy
import inspect
from typing import Any, Callable, Iterable, List
from inflection import underscore
from loguru import logger

from toolz import curry
from infra_deploy.metadata import EXISTING_FUNCS, SKIP_MEMBERS


def get_members(cls: Any) -> Iterable[Any]:
    cls_names = dir(cls)
    all_mems = dict(inspect.getmembers(cls))
    for name in cls_names:
        if name not in SKIP_MEMBERS:
            with suppress(Exception):
                yield all_mems[name]


def fn_curried(member, self, mem_name, fn_list: List[Any]):

    fn_list.append(member)
    EXISTING_FUNCS.add(mem_name)
    return fn_list


def create_existing_name(code_obj: Any, name: str):
    mdig = code_obj.co_code.hex()
    fn_name = underscore(code_obj.co_name)
    cls_name = underscore(name)
    return f"{cls_name}_{fn_name}_{mdig}"


def skip_missing(member, missing: List[str]) -> bool:
    """Skips if one of the attributes from the list is missing.

    Args:
        member ([type]): Any
        missing (List[str]): The list of items we're checking for.

    Returns:
        bool: True if we're to skip this item.
    """
    return any((not hasattr(member, x)) for x in missing)