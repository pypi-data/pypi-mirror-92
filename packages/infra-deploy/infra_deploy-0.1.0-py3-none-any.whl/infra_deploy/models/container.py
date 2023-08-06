"""
Creates, updates, and deletes a deployment using AppsV1Api.
"""

from typing import Any, Dict, List, Literal, Optional, Type

from infra_deploy.models import PullPolicy
from infra_deploy.models.base import KubeBase, KubeModel
from kubernetes import client
from kubernetes.client import V1Container, V1ResourceRequirements
from loguru import logger
from pydantic import BaseModel, ByteSize

DictStrAny = Dict[str, Any]
RecurseDictAny = Dict[str, DictStrAny]
OptBySize = Optional[ByteSize]
RESOURCE_ATTRS = V1ResourceRequirements.attribute_map


class MemCPU(BaseModel):
    memory: OptBySize
    cpu: OptBySize


class ContainerModel(KubeModel):
    __context__: str = "container"
    __api_model__: Type[V1Container] = V1Container
    name: str
    image: str
    pull_policy: str = "Always"
    ports: Dict[str, int] = {}
    resources: Dict[Literal["limits", "requests"], MemCPU] = {}

    def __init__(
        __pydantic_self__,
        *,
        name: str,
        image: str,
        ports: Dict[str,
                    int] = {},
        **data: Any
    ) -> None:
        data['name'] = name
        data['image'] = image
        data['ports'] = ports

        super().__init__(**data)

    def to_kube(self):
        return V1Container(
            name=self.name,
            image=self.image,
            image_pull_policy=self.pull_policy,
            ports=[
                client.V1ContainerPort(container_port=v)
                for v in self.ports.values()
            ],
            resources=client.V1ResourceRequirements(
                **{k: v.dict()
                   for k,
                   v in self.resources.items()}
            )
        )


class Container(KubeModel):
    # We'll take the information from decorator functions
    __api_model__: Type[V1Container] = V1Container
    name: str
    image: str
    pull_policy: PullPolicy = PullPolicy.ALWAYS
    ports: List[int] = []
    resources: Dict[str, MemCPU] = {}

    def __init__(
        __pydantic_self__,
        *,
        name: str,
        image: str,
        ports: List[int] = [],
        **data: Any
    ) -> None:
        data['name'] = name
        data['image'] = image
        data['ports'] = ports

        super().__init__(**data)

    def add_resource(self, name, **values):
        if name not in RESOURCE_ATTRS:
            raise ValueError(
                f"Item {name} isn't one of the field names [{RESOURCE_ATTRS.keys()}]"
            )

        self.resources[name] = MemCPU(**values)

    @property
    def kresources(self):
        return V1ResourceRequirements(
            **{
                k: {e: b.human_readable()
                    for e,
                    b in v.dict().items()}
                for k,
                v in self.resources.items()
            }
        )

    def to_kube(self):
        response = V1Container(
            name=self.name,
            image=self.image,
            image_pull_policy=self.pull_policy.value,
            ports=[
                client.V1ContainerPort(container_port=v) for v in self.ports
            ]
        )
        resrc = self.resources
        if not resrc:
            return response
        response.resources = self.kresources
        return response
