# from ctypes import Union
from loguru import logger
from infra_deploy.models import ApiKinds, ServiceApiVersion
from infra_deploy.models.general import Metadatable, Selectable
from typing import Any, Dict, List, Optional, Union
from kubernetes.client import V1ServiceSpec, V1Service, V1ServicePort
from pydantic import BaseModel
from infra_deploy.models.base import KubeModel
from infra_deploy.utils import (
    remove_nones_dict as cleard,
)

DictStrAny = Dict[str, Any]
RecurseDictAny = Dict[str, DictStrAny]


class MemCPU(BaseModel):
    memory: str
    cpu: str


class ServicePort(KubeModel):
    __api_model__: V1ServicePort = V1ServicePort

    port: int
    target_port: Optional[Union[str, int]]
    name: Optional[str]
    node_port: Optional[int]
    protocol: Optional[int]

    def __init__(
        self,
        *,
        port: int,
        target_port: Optional[Union[str,
                                    int]] = None,
        name: Optional[str] = None,
        node_port: Optional[int] = None,
        protocol: Optional[int] = None,
        **data: Any
    ) -> None:
        data.update(
            cleard(
                dict(
                    port=port,
                    target_port=target_port,
                    name=name,
                    node_port=node_port,
                    protocol=protocol
                )
            )
        )
        super().__init__(**data)

    def to_kube(self) -> V1ServicePort:
        _values: DictStrAny = self.get_compatible(is_convert=True)

        return V1ServicePort(**_values)


class Service(KubeModel, Metadatable, Selectable):
    __context__: str = "service"
    __service_spec__: V1ServiceSpec = V1ServiceSpec
    __api_model__: V1Service = V1Service

    api_version: ServiceApiVersion = ServiceApiVersion.V1
    ports: List[ServicePort] = []
    kind: ApiKinds = ApiKinds.SERVICE

    def __init__(self, *, name: str, **data: Any) -> None:
        super().__init__(**data)
        self.add_name(name)

    def add_name(self, name: str):
        self.add_meta("name", name)

    def add_service_port(self, **kwargs) -> ServicePort:
        return ServicePort(**kwargs)

    def to_kube(self):
        return V1Service(
            api_version=self.api_version.value,
            kind="Service",
            metadata=self.kube_meta,
            spec=V1ServiceSpec(
                selector=self.to_kube_select()['selector'],
                ports=[port.to_kube() for port in self.ports]
            )
        )

    def override_name(self, name: str):
        logger.info("overriding name")
        self.add_selector("selector", dict(app=str(name)))

    def override_image(self, img: str):
        pass

    def override_port(self, num: int):
        for p in self.ports:
            p.port = num
            p.target_port = num

    def override_service_name(self, name: str):
        self.add_name(name)