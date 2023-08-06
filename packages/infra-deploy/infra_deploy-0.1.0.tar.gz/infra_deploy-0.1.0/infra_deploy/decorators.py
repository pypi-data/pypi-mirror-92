"""
Creates, updates, and deletes a deployment using AppsV1Api.
"""
from collections import ChainMap
from collections.abc import Callable as Callable
from typing import Any
from typing import Callable
from typing import Callable as TypingCallable
from typing import Dict, Optional, Set, Union, overload

from decorator import decorate, decorator
from kubernetes.client import V1Container
from loguru import logger

from infra_deploy.constants import (
    CONTAINER_CONFIG_KEY,
    SERVICE_CONFIG_KEY,
    SPECS_CONFIG_KEY,
    VOLUME_CLAIM_CONFIG_KEY,
    VOLUME_CONFIG_KEY
)
from infra_deploy.errors import ConfigError
from infra_deploy.models import container as contain
from infra_deploy.models import deploy
from infra_deploy.utils import in_ipython

DictStrAny = Dict[str, Any]
RecurseDictAny = Dict[str, DictStrAny]
AnyCallable = TypingCallable[..., Any]
NoArgAnyCallable = TypingCallable[[], Any]

_FUNCS: Set[str] = set()


class Validator:
    __slots__ = 'func', 'pre', 'each_item', 'always', 'check_fields', 'skip_on_failure'

    def __init__(
        self,
        func: AnyCallable,
        pre: bool = False,
        each_item: bool = False,
        always: bool = False,
        check_fields: bool = False,
        skip_on_failure: bool = False,
    ):
        self.func = func
        self.pre = pre
        self.each_item = each_item
        self.always = always
        self.check_fields = check_fields
        self.skip_on_failure = skip_on_failure


def _prepare_val(function: AnyCallable, allow_reuse: bool) -> classmethod:
    """
    Avoid validators with duplicated names since without this, validators can be overwritten silently
    which generally isn't the intended behaviour, don't run in ipython (see #312) or if allow_reuse is False.
    """
    f_cls = function if isinstance(function,
                                   classmethod) else classmethod(function)
    if not in_ipython() and not allow_reuse:
        ref = f_cls.__func__.__module__ + '.' + f_cls.__func__.__qualname__
        # logger.info(ref)
        if ref in _FUNCS:
            raise ConfigError(
                f'duplicate validator function "{ref}"; if this is intended, set `allow_reuse=True`'
            )
        _FUNCS.add(ref)
    return f_cls


def _set_fn_attr(f: Callable[..., classmethod], CNF_KEY):
    pre = False
    skip_on_failure = False
    allow_reuse = True
    f_cls = _prepare_val(f, allow_reuse)
    setattr(
        f_cls,
        CNF_KEY,
        Validator(
            func=f_cls.__func__,
            pre=pre,
            skip_on_failure=skip_on_failure
        )
    )
    return f_cls


# @overload
# def container(_func: AnyCallable) -> classmethod:
#     ...

# @overload
# def container(
#     *,
#     name: str = "",
# ) -> Callable[[AnyCallable],
#               classmethod]:
#     ...


def container(
    _func: Optional[AnyCallable] = None,
    *,
    name: str = ""
) -> Union[classmethod,
           Callable[[AnyCallable],
                    classmethod]]:
    """
    Decorate methods on a model indicating that they should be used to validate (and perhaps modify) data either
    before or after standard model parsing/validation is performed.
    """
    if _func:
        return _set_fn_attr(_func, CONTAINER_CONFIG_KEY)

    def dec(f: AnyCallable) -> classmethod:
        return _set_fn_attr(f, CONTAINER_CONFIG_KEY)

    return dec


def specifics(
    _func: Optional[AnyCallable] = None,
    *,
    name: str = ""
) -> Union[classmethod,
           Callable[[AnyCallable],
                    classmethod]]:
    """
    Decorate methods on a model indicating that they should be used to validate (and perhaps modify) data either
    before or after standard model parsing/validation is performed.
    """

    if _func:
        return _set_fn_attr(_func, SPECS_CONFIG_KEY)

    def dec(f: AnyCallable) -> classmethod:
        return _set_fn_attr(f, SPECS_CONFIG_KEY)

    return dec


def service(
    _func: Optional[AnyCallable] = None,
    *,
    name: str = ""
) -> Union[classmethod,
           Callable[[AnyCallable],
                    classmethod]]:
    """
    Decorate methods on a model indicating that they should be used to validate (and perhaps modify) data either
    before or after standard model parsing/validation is performed.
    """
    if _func:
        return _set_fn_attr(_func, SERVICE_CONFIG_KEY)

    def dec(f: AnyCallable) -> classmethod:
        return _set_fn_attr(f, SERVICE_CONFIG_KEY)

    return dec


def template(
    _func: Optional[AnyCallable] = None,
    *,
    name: str = ""
) -> Union[classmethod,
           Callable[[AnyCallable],
                    classmethod]]:
    """
    Decorate methods on a model indicating that they should be used to validate (and perhaps modify) data either
    before or after standard model parsing/validation is performed.
    """
    if _func:
        return _set_fn_attr(_func, SPECS_CONFIG_KEY)

    def dec(f: AnyCallable) -> classmethod:
        return _set_fn_attr(f, SPECS_CONFIG_KEY)

    return dec


def volume(
    _func: Optional[AnyCallable] = None,
    *,
    name: str = ""
) -> Union[classmethod,
           Callable[[AnyCallable],
                    classmethod]]:
    """
    Decorate methods on a model indicating that they should be used to validate (and perhaps modify) data either
    before or after standard model parsing/validation is performed.
    """
    if _func:
        return _set_fn_attr(_func, VOLUME_CONFIG_KEY)

    def dec(f: AnyCallable) -> classmethod:
        return _set_fn_attr(f, VOLUME_CONFIG_KEY)

    return dec


def volume_claim(
    _func: Optional[AnyCallable] = None,
    *,
    name: str = ""
) -> Union[classmethod,
           Callable[[AnyCallable],
                    classmethod]]:
    """
    Decorate methods on a model indicating that they should be used to validate (and perhaps modify) data either
    before or after standard model parsing/validation is performed.
    """
    if _func:
        return _set_fn_attr(_func, VOLUME_CLAIM_CONFIG_KEY)

    def dec(f: AnyCallable) -> classmethod:
        return _set_fn_attr(f, VOLUME_CLAIM_CONFIG_KEY)

    return dec
