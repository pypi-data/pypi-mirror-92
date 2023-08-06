"""
Creates, updates, and deletes a deployment using AppsV1Api.
"""
import abc
import inspect
import hashlib
import orjson
from typing import Any, AnyStr, Dict, List, Optional, Union

from inflection import underscore, camelize
import yaml
from infra_deploy import (
    utils,
    PropertyBaseModel,
)
from infra_deploy.metadata import (
    EXISTING_FUNCS,
    create_existing_name,
    get_members,
    skip_missing
)
from infra_deploy.typings import AnyCallable
from kubernetes import client as kli
from loguru import logger
from pydantic import BaseModel, Extra, PrivateAttr
from decorator import decorate

# from functools import cached_property
from cytoolz.dicttoolz import keyfilter
from cachetools import cached, cachedmethod, LRUCache, MRUCache
from devtools import debug
# from infra_deploy.models import (
#     Service,
# )
# from infra_deploy.models.deploy import Deployment

DictStrAny = Dict[str, Any]    # type: ignore
RecurseDictAny = Dict[str, DictStrAny]
object_setattr = object.__setattr__


def _memoize(func, *args, **kw):
    if kw:    # frozenset is used to ensure hashability
        key = args, frozenset(kw.items())
    else:
        key = args
    cache = func.cache    # attribute added by memoize
    if key not in cache:
        cache[key] = func(*args, **kw)
    return cache[key]


def memoize(f):
    """
     A simple memoize implementation. It works by adding a .cache dictionary
     to the decorated function. The cache will grow indefinitely, so it is
     your responsibility to clear it, if needed.
     """
    f.cache = {}
    return decorate(f, _memoize)


class ExtraBase(PropertyBaseModel, abc.ABC):

    __ports__: DictStrAny = {}

    class Config:
        extra = Extra.allow


class GeneralAPI(ExtraBase, abc.ABC):
    @abc.abstractmethod
    def to_kube(
        self
    ) -> Union[kli.V1Deployment,
               kli.CoreApi,
               kli.CoreV1Api,
               kli.CustomObjectsApi]:
        raise NotImplementedError("Kubernetes object not created.")

    def config_dict(self) -> Dict[AnyStr, AnyStr]:
        return utils.remove_nones_dict(self.to_kube().to_dict())

    @abc.abstractmethod
    def to_dict(self) -> Dict[AnyStr, AnyStr]:
        raise NotImplementedError("To dict is not implemented.")


class OverrideSupport(abc.ABC):
    def override_port(self, num: int):
        pass

    def override_name(self, name: str):
        pass

    def override_image(self, img: str):
        pass

    def override_service_name(self, name: str):
        pass


class KubeBase(PropertyBaseModel, OverrideSupport, abc.ABC):
    __context__: str
    # A list of strings that say which children are allowed
    __allowed__: List[str] = []
    __test_root__: List[Any] = []
    __kube_model__: Optional[Any] = None

    __container_methods__: List[AnyCallable] = []
    __service_methods__: List[AnyCallable] = []
    __spec_methods__: List[AnyCallable] = []
    __volume_methods__: List[AnyCallable] = []
    __volume_claim_methods__: List[AnyCallable] = []

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        for getter, setter in self.get_properties():
            if getter in data and setter:
                getattr(type(self), setter).fset(self, data[getter])

    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True

    @classmethod
    def methods_with_decorator(cls, decorator_name):
        sourcelines = inspect.getsourcelines(cls)[0]
        for i, line in enumerate(sourcelines):
            line = line.strip()
            if line.split('(')[0].strip(
            ) == '@' + decorator_name:    # leaving a bit out
                next_line = sourcelines[i + 1]
                name = next_line.split('def')[1].split('(')[0].strip()
                yield (name)

    @classmethod
    def set_containers(cls, cls_):
        attrs = cls_.methods_with_decorator("container")
        attrs = list(attrs)
        for attr in attrs:
            result = getattr(cls_, attr)
            cls_.__container_methods__.append(result)

    @classmethod
    def set_specs(cls, cls_):
        # TODO: Figure out how to prevent using list. It will cause a slowdown.
        attrs = cls_.methods_with_decorator("specifics")
        attrs = list(attrs)
        for attr in attrs:
            result = getattr(cls_, attr)
            cls_.__spec_methods__.append(result)

    @classmethod
    def set_volume(cls, cls_):
        attrs = cls_.methods_with_decorator("volume")
        attrs = list(attrs)
        for attr in attrs:
            result = getattr(cls_, attr)
            cls_.__volume_methods__.append(result)

    @classmethod
    def set_volume_claim(cls, cls_):
        attrs = cls_.methods_with_decorator("volume_claim")
        attrs = list(attrs)
        for attr in attrs:
            result = getattr(cls_, attr)
            cls_.__volume_claim_methods__.append(result)

    @classmethod
    def set_services(cls, cls_):
        attrs = cls_.methods_with_decorator("service")
        attrs = list(attrs)
        for attr in attrs:
            result = getattr(cls_, attr)
            cls_.__service_methods__.append(result)

    @classmethod
    def get_container_mems(cls, cls_):
        mems = inspect.getmembers(cls_, predicate=inspect.ismethod)
        return mems

    # def __new__(cls, *args, **kwargs) -> Any:
    #     # mcs, name, bases, namespace, **kwargs
    #     # cls
    #     __mod__ = super().__new__(cls)

    #     ms = cls.get_container_mems(__mod__)
    #     # for m in ms:
    #     cls.set_containers(__mod__)
    #     cls.set_services(__mod__)
    #     cls.set_specs(__mod__)
    #     cls.set_volume(__mod__)
    #     cls.set_volume_claim(__mod__)
    #     return __mod__

    @abc.abstractmethod
    def to_kube(self) -> kli.V1Deployment:
        raise NotImplementedError

    def config_dict(self) -> Dict[AnyStr, AnyStr]:
        return utils.remove_nones_dict(self.to_kube().to_dict())

    def to_dict(self):
        return self.config_dict()

    def override_port(self, num: int):
        pass

    def override_name(self, name: str):
        pass

    def override_image(self, img: str):
        pass


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


@cached(cache=LRUCache(maxsize=1024))
def mem_api_hash(api_attrs: Dict[str, str]):
    converted = dict(api_attrs)
    return hashlib.md5(orjson.dumps(converted))


class KubeModel(PropertyBaseModel, OverrideSupport, abc.ABC):
    __context__: str
    # A list of strings that say which children are allowed
    __allowed__: List[str] = []
    __test_root__: List[Any] = []
    __api_model__: Optional[Any] = None

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        for getter, setter in self.get_properties():
            if getter in data and setter:
                getattr(type(self), setter).fset(self, data[getter])

    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        use_enum_values = True

    def __new__(cls, *args, **kwargs) -> Any:
        # mcs, name, bases, namespace, **kwargs
        # cls
        self = super().__new__(cls)
        api_model = getattr(self, "__api_model__", None)
        if api_model is None:
            raise AttributeError(
                "All kubernetes models are supposed to have an api model"
            )
        return self

    @property
    def attr_map(self):
        return self.in_mem_attr_map()

    @property
    def __attribute_map(self):
        return getattr(self.__api_model__, "attribute_map", {})

    @property
    def ctx(self):
        return self.__context__

    # @cachedmethod(cache={})
    def in_mem_attr_map(self) -> Dict[str, str]:
        """Publically facing function. Use

        Returns:
            Dict[str, str]: [description]
        """
        return self.__attribute_map

    def add_attribute(self, key: str, val: Any):
        if key in self.attr_map:
            setattr(self, key, val)

    @abc.abstractmethod
    def to_kube(self) -> kli.V1Deployment:
        raise NotImplementedError

    def config_dict(self) -> Dict[AnyStr, AnyStr]:
        kube_obj = self.to_kube()
        if isinstance(kube_obj, dict):
            return kube_obj

        mappings = kube_obj.attribute_map
        init_dict = utils.remove_nones_dict(kube_obj.to_dict())

        return utils.map_fields(init_dict, mappings)

    def to_dict(self):
        return self.config_dict()

    # @memoize
    def get_hash_str(self, place: int):
        return mem_api_hash(frozenset(self.__attribute_map.items()))

    def get_compatible(self, is_convert: bool = False) -> DictStrAny:
        """Gets the compatible attributes from the class and returns them.

        Returns:
            DictStrAny: All items that are in the attribute map.
        """
        _allvars = dir(self)
        _attr_list: List[str] = list(self.attr_map.keys())
        remainder: Dict[str,
                        Any] = keyfilter(lambda x: x in _attr_list,
                                         _allvars)
        if not is_convert:
            return remainder
        return self.__convert_compatiable(remainder)

    def __convert_compatiable(self, items: DictStrAny):
        response = {}
        for k, v in items.items():
            if isinstance(v, KubeModel):
                response[k] = v.to_kube()

                continue
            response[k] = v

        return response

    def __hash__(self) -> int:
        return hash(self.get_hash_str(1))

    def override_port(self, num: int):
        pass

    def override_name(self, name: str):
        pass

    def override_image(self, img: str):
        pass


def check_callable(member: Any) -> bool:
    has_callable = hasattr(member, 'is_callable')
    if has_callable:
        if getattr(member, "is_callable"):
            return True
    return False


class Precompiled(ExtraBase):
    container: List[Any] = []
    template: List[Any] = []
    deployment: List[Any] = []
    service: List[Any] = []
    ambassador: List[Any] = []
    not_exist: List[Any] = []

    @property
    def is_compile(self) -> bool:
        values = self.dict()
        for k, v in values.items():
            if len(v) > 0:
                return True
        return False

    @property
    def first_task(self):
        if self.service:
            return "service"
        elif self.deployment:
            return "deployment"


# class CompiledConfigs(ExtraBase):
#     container: List[Any] = []
#     template: List[Any] = []
#     deployment: List[Any] = []
#     service: List[Any] = []
#     ambassador: List[Any] = []
#     not_exist: List[Any] = []


class Precompiled(ExtraBase):
    container: List[Any] = []
    template: List[Any] = []
    deployment: List[Any] = []
    service: List[Any] = []
    ambassador: List[Any] = []
    not_exist: List[Any] = []

    @property
    def is_compile(self) -> bool:
        values = self.dict()
        for k, v in values.items():
            if len(v) > 0:
                return True
        return False

    @property
    def first_task(self):
        if self.service:
            return "service"
        elif self.deployment:
            return "deployment"


PRE_COMP_KEYS = (Precompiled.__fields__.keys())
COMPUTE_ORDER = ["service", "deployment", "template", "container"]
COMPILED_VALUES = {}


def add_behavior(precomp: Precompiled, member: Any) -> Precompiled:
    behave = getattr(member, "__behavior_type__", "not_exist")
    current_state: List[Any] = getattr(precomp, behave, [])
    current_state.append(member)
    setattr(precomp, behave, current_state)
    return precomp


class Composition(ExtraBase, abc.ABC):
    # Using this new codebase to manage the parts of a workflow.

    # The use case will be to create a full ambassador deployment as seen here
    # https://github.com/kubernetes-client/python/blob/master/examples/ingress_create.py
    # We're essentially building on this.

    # TODO: We're going to
    __precomp_dict__: Dict[str, Precompiled] = {}
    __tasks__: List[Any] = PrivateAttr(default=[])
    __response__: List[DictStrAny] = []
    # __compiled__:

    name: Optional[str] = None
    service_name: Optional[str] = None
    image: Optional[str] = None
    port: Optional[int] = None

    def __new__(cls, **kwargs):
        print("")
        self: 'Composition' = super().__new__(cls)

        current_precomp: Precompiled = None
        name = self.__class__.__name__
        cls_name = underscore(name)
        agg_str_set = []
        lazy_compute = []
        for member in get_members(cls):
            if skip_missing(member, ["__code__"]):
                continue
            if not check_callable(member):
                continue
            SPOOKY = create_existing_name(member.__code__, cls_name)
            agg_str_set.append(SPOOKY)
            if SPOOKY in EXISTING_FUNCS:
                lazy_compute.append(member)
                continue
            EXISTING_FUNCS.add(SPOOKY)
            if not current_precomp:
                # Lazily create a precompiled variable if there's an unknown variable
                current_precomp = Precompiled()
            # This could be converted into a single function.
            current_precomp = add_behavior(current_precomp, member)

        j_based: str = utils.b64_ls(agg_str_set)
        if j_based in self.__precomp_dict__ or j_based == "" or current_precomp is None:
            return self

        if len(lazy_compute) > 0:
            for lazy_mem in lazy_compute:
                current_precomp = add_behavior(current_precomp, lazy_mem)
                # EXISTING_FUNCS.add(SPOOKY)

        self.__precomp_dict__[j_based] = current_precomp
        return self

    def __init__(
        self,
        name: Optional[str] = None,
        image: Optional[str] = None,
        port: Optional[int] = None,
        service_name: Optional[str] = None,
        **data
    ):
        # Here we'll compile the code base
        if name is not None:
            data["name"] = name

        if image is not None:
            data["image"] = image

        if port is not None:
            data["port"] = port

        if service_name is not None:
            data["service_name"] = service_name

        super().__init__(**data)
        if not self.__precomp_dict__:
            return

        self.compile()

    def to_kube(self) -> Any:
        raise NotImplementedError

    def config_dict(self) -> Dict[AnyStr, AnyStr]:
        return utils.remove_nones_dict(self.to_kube().to_dict())

    def to_dict(self):
        return self.config_dict()

    def __hash__(self) -> int:
        # d = super().dict()
        # keys = d.keys()
        return hash(self.__class__.__name__)

    def __str__(self) -> str:
        cname = self.__class__.__name__
        rlen = len(self.__response__)
        return f"{cname}(doc_num={rlen})"

    def to_yaml(self) -> str:
        return yaml.dump_all(self.__response__)

    def compile(self):
        logger.success(self.__fields__)
        configs = []
        for key, precomp in self.__precomp_dict__.items():
            # for usable in ["deployment", "service"]:
            # logger.warning(precomp)
            if not precomp.service and not precomp.deployment:
                continue
            main_confs = precomp.service + precomp.deployment
            for srv in main_confs:
                srvs: OverrideSupport = srv(self)

                if self.name:
                    srvs.override_name(self.name)
                if self.image:
                    srvs.override_image(self.image)
                if self.port:
                    srvs.override_port(self.port)

                if self.service_name:
                    srvs.override_service_name(self.service_name)
                configs.append(srvs.to_dict())
        self.__response__ = configs

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError
        # func()


class TestInit(KubeBase):
    __context__: str = "deployment"
    __allowed__: List[str] = ["spec"]

    app_version: int = 1
    kind: str = "Deployment"
    replicas: int = 4

    def __init__(self, **data: Any):
        super(TestInit, self).__init__(**data)


class TestUpdatedBase(Composition):
    outside_port: int = 7159

    def to_kube(self) -> Any:
        return kli.V1Container(
            name="deployment",
            image="gcr.io/google-appengine/fluentd-logger",
            image_pull_policy="Never",
            ports=[kli.V1ContainerPort(container_port=self.outside_port)],
        )


if __name__ == "__main__":
    outside = TestUpdatedBase()
    logger.success(outside.to_dict())
    # logger.info(getattr(outside, "__fieldset__"))
