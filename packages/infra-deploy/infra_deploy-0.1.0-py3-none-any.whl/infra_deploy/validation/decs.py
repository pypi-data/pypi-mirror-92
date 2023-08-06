# import infra_deploy
# from infra_deploy import Deployment

# Deployment = infra_deploy.Deployment
from typing import Any, Optional, Tuple, Type
from loguru import logger
from pydantic import BaseModel
from pydantic.fields import ModelField
from decorator import contextmanager
from infra_deploy.models.specs import SpecDeploy, SpecPodTemplate, SpecPod
from infra_deploy.models.enums import SpecTypes


class SimpleGet:
    def __init__(self, mod_cls: Optional[BaseModel]):
        self.mod_cls = mod_cls

    def get_mod(self, name: str) -> Tuple[ModelField, Any]:
        if self.mod_cls is None:
            raise AttributeError
        s = self.mod_cls.__fields__[name]
        d = s.default
        return s, d

    def set_mod(self, name: str, value: Any):
        if self.mod_cls is None:
            raise AttributeError
        self.mod_cls.__fields__[name] = value
        return super().__setattr__(name, value)


@contextmanager
def managed_resource(
    *args,
    name: str = "containers",
    cls_: BaseModel = None,
    expected: type = list,
    **kwds
):
    # Code to acquire resource, e.g.:
    # resource = acquire_resource(*args, **kwds)
    simp = SimpleGet(cls_)
    field, dflt = simp.get_mod(name)
    if not isinstance(dflt, expected):
        raise TypeError(f"Was supposed to find a {expected.__name__}")
    try:
        yield dflt
    finally:
        field.default = dflt
        simp.set_mod(name, field)
        # Code to release resource, e.g.:
        # release_resource(resource)

        # return super().__getattribute__(name)


def add_container_objects(cls_):
    with managed_resource(cls_=cls_, expected=list) as default:
        for container in cls_.__container_methods__:
            default.append(container())


def add_service_objects(cls_):
    with managed_resource(name="services", cls_=cls_, expected=list) as default:
        for service in cls_.__service_methods__:
            default.append(service())


def add_volume_claim_objects(cls_):

    with managed_resource(
        name="volume_claims",
        cls_=cls_,
        expected=list
    ) as default:
        for volume_claim in cls_.__volume_claim_methods__:
            default.append(volume_claim())


def add_volume_objects(cls_):
    with managed_resource(name="volumes", cls_=cls_, expected=list) as default:
        for volume in cls_.__volume_methods__:
            default.append(volume())


def add_spec_objects(cls_):
    with managed_resource(
        name="specs_dict",
        cls_=cls_,
        expected=dict
    ) as default:
        for spec in cls_.__spec_methods__:
            lspec = spec()
            if isinstance(lspec, SpecDeploy):
                default[SpecTypes.DEPLOY] = lspec

            if isinstance(lspec, SpecPodTemplate):
                default[SpecTypes.POD_TEMPLATE] = lspec

            if isinstance(lspec, SpecPod):
                default[SpecTypes.POD] = lspec