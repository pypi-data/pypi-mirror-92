import abc
from infra_deploy.models.enums import ResourceTypes
import inspect
import re
from abc import ABCMeta
from contextlib import suppress
from typing import Any, Callable, Dict, List, Optional

import addict as ad
from decopatch import DECORATED, F_ARGS, F_KWARGS, WRAPPED, function_decorator
from decorator import contextmanager, decorate, decorator
from inflection import underscore
from infra_deploy.metadata import (
    EXISTING_FUNCS,
    create_existing_name,
    fn_curried,
    get_members,
    skip_missing
)
from loguru import logger
from pydantic import BaseModel, Field, validate_arguments
from toolz import curry

object_setattr = object.__setattr__
OptStr = Optional[str]


# We'd use this kind of decorator to position variables we'll need to run the compile function.
@function_decorator    # type: ignore
def container():
    """
    Example decorator to add a 'tag' attribute to a function. 
    :param tag: the 'tag' value to set on the decorated function (default 'hi!).
    """
    def _apply_decorator(f):
        """
        This is the method that will be called when `@general` is used on a 
        function `f`. It should return a replacement for `f`.
        """
        object_setattr(f, 'is_callable', True)
        object_setattr(f, 'item_type', "container")

        return f

    return _apply_decorator


def __base_memoize(func, *args, **kwargs):
    if kwargs:    # frozenset is used to ensure hashability
        key = args, frozenset(kwargs.items())
    else:
        key = args
    cache = func.cache    # attribute added by memoize
    if key not in cache:
        cache[key] = func(*args, **kwargs)
    return cache[key]


def _template(func, *args, **kwargs):
    func.__behavior_type__ = "template"
    func.is_callable = True
    return __base_memoize(func, *args, **kwargs)


# @function_decorator
# def metaitem(name: str, f=WRAPPED, f_args=F_ARGS, f_kwargs=F_KWARGS, **itemval):

#     outcome = f(*f_args, **f_kwargs)
#     if not hasattr(outcome, "add_meta"):
#         logger.info("Not able to add metadata")
#         return outcome
#     outcome.add_meta(name, itemval)
#     return outcome

# @function_decorator
# def metagroups(f=WRAPPED, f_args=F_ARGS, f_kwargs=F_KWARGS, **metatags):

#     outcome = f(*f_args, **f_kwargs)
#     if not hasattr(outcome, "add_meta"):
#         logger.info("Not able to add metadata")
#         return outcome
#     [outcome.add_meta(k, v) for k, v in metatags.items()]
#     return outcome


@function_decorator()
def resource(
    name: ResourceTypes,
    memory: OptStr = None,
    cpu: OptStr = None,
    f=WRAPPED,
    f_args=F_ARGS,
    f_kwargs=F_KWARGS
):

    outcome = f(*f_args, **f_kwargs)
    if not hasattr(outcome, "add_resource"):
        # logger.info("This isn't one of the the fields we're allowed to add a resource on.")
        return outcome
    agg = {}
    if memory:
        agg['memory'] = memory
    if cpu:
        agg['cpu'] = cpu

    outcome.add_resource(name, **agg)
    return outcome


@decorator    # type: ignore
def ports(func: Callable, ports: List[int] = [], *args, **kwargs):
    """
    Example decorator to add a 'tag' attribute to a function. 
    :param tag: the 'tag' value to set on the decorated function (default 'hi!).
    """
    response = func(*args, **kwargs)
    if ports and hasattr(response, "ports"):
        curr = response.ports
        response.ports = curr + ports
    return response
