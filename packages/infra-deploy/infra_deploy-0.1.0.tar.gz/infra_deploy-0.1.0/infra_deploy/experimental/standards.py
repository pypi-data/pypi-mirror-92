import abc
import inspect
import typing

from functools import partial
from functools import wraps

from typing import Any
from typing import Callable
from typing import Dict
from typing import Generic
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from inflection import camelize
from inflection import dasherize
from inflection import underscore

from infra_deploy import ContainerModel as Container
from infra_deploy.models.container import MemCPU
from pydantic import BaseModel
from loguru import logger
from decorator import decorator
from decopatch import function_decorator

T = TypeVar("T")


class SpecProxy(object):
    """Spec Proxy.

    NOTE: This class is not meant to be used directly.
    """
    def __new__(cls, spec: "Spec", obj: Any, callable: bool):
        self = super(SpecProxy, cls).__new__(cls)

        self._obj = obj
        self._spec = spec

        self._callable = callable

        return self

    def __call__(self, *args, **kwargs):
        spec: "Spec" = self._spec

        T = Type[spec.__model__]

        if self._callable:
            ret: Any = spec.fget(self._obj, *args, **kwargs)

            if hasattr(spec.__model__, "swagger_types"):
                for attr, swagger_type in spec.__model__.swagger_types.items():
                    t: Any = getattr(models, swagger_type, None)
                    if t == type(ret):
                        setattr(spec, attr, ret)
                        break
            else:
                for attr, openapi_type in spec.__model__.openapi_types.items():
                    t: Any = getattr(models, openapi_type, None)
                    if t == type(ret):
                        setattr(spec, attr, ret)
                        break

            spec.__init_model__(ret, *args, **kwargs)

        attr_dict: Dict[str,
                        Any] = {
                            k: spec.__dict__[k]
                            for k in spec.__model__.attribute_map
                        }
        model: T = spec.__model__(**attr_dict)

        self._spec.model = model

        return model


class Spec(property):
    """Base class for Workflow Specs.
    NOTE: This class is not meant to be used directly.
    """
    __model__ = "POOPY"

    def __new__(cls, f: Callable[..., T]):
        self = super().__new__(cls, f)
        self.__callable = True
        self.__compiled_model = None

        sig: inspect.Signature = inspect.signature(f)
        setattr(self, "__signature__", sig)
        setattr(self, "my_attr", 'FOO')
        print(self)
        return self

    def __call__(self, *args, **kwargs) -> T:
        # This function is required for the call signature and should NOT be called
        raise NotImplementedError("This function shouldn't be called directly.")

    def __get__(self, obj: Any, objtype: Any = None, **kwargs):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(f"Unreadable attribute '{self.fget}'")
        return SpecProxy(self, obj, callable=self.__callable)


class example(Spec):
    """Base class for Workflow Specs.
    NOTE: This class is not meant to be used directly.
    """
    pass


# Create a service function and deployment function.
# Use those decorators to set the stage for the system.
def decfactory(param1, param2, *args, **kwargs):
    def caller(f, *args, **kw):
        return somefunc(f, param1, param2, *args, **kwargs)

    return decorator(caller)


class Declaration(BaseModel, abc.ABC):
    # we're using basemodel as the base.

    def __init__(__pydantic_self__, **data: Any) -> None:

        super().__init__(**data)
        __pydantic_self__.compile()

    def compile(self):
        logger.debug("Compiling here")

    def __new__(cls) -> Any:
        return super().__new__(cls)


class DeclarationMeta(abc.ABCMeta):
    # we're using basemodel as the base.

    def __new__(cls, name: str, bases, props: Dict[str, Any]):
        # Check for tagged members
        logger.info(name)
        logger.warning(bases)
        logger.success(props)
        has_tag = False
        for member in props.values():
            is_model = hasattr(member, '__model__')

            if hasattr(member, 'my_attr'):
                has_tag = True
                break
        if has_tag:
            # Set the class attribute
            props['my_attr'] = 'FOO BAR'
        # Now let 'type' actually allocate the class object and go on with life
        return super().__new__(cls, name, bases, props)


def dipshit(method):
    "Decorate the method with an attribute to let the metaclass know it's there."
    method.my_attr = 'FOO BAR'
    return method    # No need for a wrapper, we haven't changed


def cuntshit(Spec):
    "Decorate the method with an attribute to let the metaclass know it's there."
    # How the fuck does this work?
    pass    # No need for a wrapper, we haven't changed


@function_decorator
def add_tag(tag='hi!'):
    """
    Example decorator to add a 'tag' attribute to a function. 
    :param tag: the 'tag' value to set on the decorated function (default 'hi!).
    """
    def _apply_decorator(f):
        """
        This is the method that will be called when `@add_tag` is used on a 
        function `f`. It should return a replacement for `f`.
        """
        setattr(f, 'tag', tag)
        return f

    return _apply_decorator
