from typing import Any, Dict, Literal, Optional, TypedDict, Union

from auto_all import end_all, start_all
from decopatch import F_ARGS, F_KWARGS, WRAPPED, function_decorator
from decorator import decorator

from infra_deploy.models.base import DictStrAny
from infra_deploy.utils import remove_nones_dict as clrd
from infra_deploy.models import Service
from loguru import logger
from makefun import with_signature, create_function

object_setattr = object.__setattr__
OptStr = Optional[str]

start_all(globals())


@function_decorator()
# @with_signature('selector(name:str, **itemval)')
def selector(name: str, f=WRAPPED, f_args=F_ARGS, f_kwargs=F_KWARGS, **itemval):

    result = f(*f_args, **f_kwargs)
    if not hasattr(result, "add_selector"):
        logger.info("Not able to add a selector")
        return result
    result.add_selector(name, itemval)
    return result


@function_decorator()
def generalize(f=WRAPPED, f_args=F_ARGS, f_kwargs=F_KWARGS, **metatags):
    """Add an attribute to the given model. The attribute must exist inside of the attribute map.

    Args:
        f (Callable, optional): [description]. Defaults to WRAPPED.
        f_args ([type], optional): [description]. Defaults to F_ARGS.
        f_kwargs ([type], optional): [description]. Defaults to F_KWARGS.

    Returns:
        Any: The called function. Should have an added attribute we want.
    """
    result = f(*f_args, **f_kwargs)

    if not hasattr(result, "add_attribute"):
        # logger.info("Not able to add metadata")
        return result
    # [result.add_attribute(k, v) for k, v in metatags.items()]
    for k, v in metatags.items():
        result.add_attribute(k, v)
    return result


@function_decorator(enable_stack_introspection=True)
def metaitem(name: str, f=WRAPPED, f_args=F_ARGS, f_kwargs=F_KWARGS, **itemval):

    outcome = f(*f_args, **f_kwargs)
    if not hasattr(outcome, "add_meta"):
        logger.info("Not able to add metadata")
        return outcome
    outcome.add_meta(name, itemval)
    return outcome


@function_decorator()
def metagroups(f=WRAPPED, f_args=F_ARGS, f_kwargs=F_KWARGS, **metatags):

    outcome = f(*f_args, **f_kwargs)
    if not hasattr(outcome, "add_meta"):
        logger.info("Not able to add metadata")
        return outcome
    [outcome.add_meta(k, v) for k, v in metatags.items()]
    return outcome


@with_signature("name(name:str, *args, **kwargs)")
@function_decorator(enable_stack_introspection=True)
def name(name: str, func=WRAPPED, f_args=F_ARGS, f_kwargs=F_KWARGS):

    outcome = func(*f_args, **f_kwargs)
    if not hasattr(outcome, "add_name"):
        logger.info("Not able to add metadata")
        return outcome
    outcome.add_name(name)
    return outcome


@function_decorator(enable_stack_introspection=True)
def serve_port(
    *,
    port: int,
    target_port: Optional[Union[str,
                                int]] = None,
    name: Optional[str] = None,
    node_port: Optional[int] = None,
    protocol: Optional[int] = None,
    func=WRAPPED,
    f_args=F_ARGS,
    f_kwargs=F_KWARGS
):

    if port is None:
        raise ValueError("The port cannot be empty ")
    cleared_port_values: DictStrAny = clrd(
        dict(
            port=port,
            target_port=target_port,
            name=name,
            node_port=node_port,
            protocol=protocol
        )
    )
    # kwargs.update(cleared_values)
    outcome = func(*f_args, **f_kwargs)

    if not isinstance(outcome, Service):
        logger.info("Not able to add metadata")
        raise TypeError(
            "serve_port is a specialized function and should be an instance of Service"
        )
    outcome.add_service_port(**cleared_port_values)
    return outcome


# SERVE_SIGNATURE = "serve_port(port: int, target_port: Optional[Union[str,int]] = None, name: Optional[str] = None, node_port: Optional[int] = None, protocol: Optional[int] = None, *args, **kwargs)"

# serve_port = create_function(SERVE_SIGNATURE, _serve_port)

# @decorator
# def name(func, item_name: str, *args, **kwargs):

#     outcome = func(*args, **kwargs)
#     if not hasattr(outcome, "add_name"):
#         logger.info("Not able to add metadata")
#         return outcome
#     outcome.add_name(item_name)
#     return outcome

end_all(globals())
