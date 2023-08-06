from typing import Optional

from decopatch import F_ARGS, F_KWARGS, WRAPPED, function_decorator
from decorator import decorator, decorate
from loguru import logger
from auto_all import start_all, end_all

start_all(globals())


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


def template(f):
    """Template

    Args:
        f (Callable): The function we're decorating with.

    Returns:
        _Func@decorate: A decorated function.
    """
    f.cache = {}
    return decorate(f, _template)


def _container(func, *args, **kwargs):
    response = __base_memoize(func, *args, **kwargs)
    return response


def container(func):
    """Behavioral decorator for the container type.

    Args:
        f (Callable): The function we're decorating with.

    Returns:
        _Func@decorate: A decorated function.
    """
    func.cache = {}
    func.__behavior_type__ = "container"
    func.is_callable = True
    return decorate(func, _container)


def _deployment(func, *args, **kwargs):
    response = __base_memoize(func, *args, **kwargs)

    return response


def deployment(func):
    """Behavioral decorator for deployment

    Args:
        f (Callable): The function we're decorating with.

    Returns:
        _Func@decorate: A decorated function.
    """
    func.cache = {}
    func.__behavior_type__ = "deployment"
    func.is_callable = True
    return decorate(func, _deployment)


def _service(func, *args, **kwargs):
    """Service behavior function.

    Args:
        func (Callable): Function we're modifying behavior for.

    Returns:
        Callable: Activated function with slightly modified behavior.
    """
    response = __base_memoize(func, *args, **kwargs)
    return response


def service(func):
    """Behavioral decorator for the service type.

    Args:
        f (Callable): The function we're decorating with.

    Returns:
        _Func@decorate: A decorated function.
    """
    func.cache = {}
    func.__behavior_type__ = "service"
    func.is_callable = True
    return decorate(func, _service)


def _ambassador(func, *args, **kwargs):
    response = __base_memoize(func, *args, **kwargs)

    return response


def ambassador(func):
    """Behavioral decorator for the ambassador type.

    Args:
        f (Callable): The function we're decorating with.

    Returns:
        _Func@decorate: A decorated function.
    """
    func.cache = {}
    func.__behavior_type__ = "ambassador"
    func.is_callable = True
    return decorate(func, _ambassador)


end_all(globals())
