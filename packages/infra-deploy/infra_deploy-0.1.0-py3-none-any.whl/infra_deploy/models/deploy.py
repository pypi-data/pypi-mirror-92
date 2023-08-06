# from __future__ import annotations

from typing import Any, AnyStr, Dict, List, Literal, Optional
from loguru import logger

import yaml
from infra_deploy.helpers import built_test_deploy
from infra_deploy.models.general import Metadatable, Selectable
from infra_deploy.models.base import KubeBase, KubeModel
from infra_deploy.models.container import ContainerModel
from infra_deploy.models.enums import SpecTypes
from infra_deploy.models.specs import BaseSpec, SpecPodTemplate
from infra_deploy.validation import decs
from kubernetes import client as kli
from kubernetes.client import V1Deployment, V1DeploymentSpec


class Deployment(KubeModel, Metadatable, Selectable):
    __api_model__: V1Deployment = V1Deployment
    api_version: str = "apps/v1"
    kind: str = "Deployment"
    template: SpecPodTemplate

    replicas: int = 3

    def __init__(
        self,
        template: SpecPodTemplate,
        *,
        api_version: Optional[str] = None,
        kind: Optional[str] = None,
        replicas: Optional[int] = None,
        **data: Any
    ) -> None:
        data['template'] = template

        if api_version:
            data['api_version'] = api_version

        if kind:
            data['kind'] = kind

        if replicas:
            data['replicas'] = replicas

        super().__init__(**data)

    def add_name(self, name: str):
        self.add_meta("name", name)

    def to_kube(self) -> V1Deployment:
        return V1Deployment(
            api_version=self.api_version,
            kind=self.kind,
            metadata=self.kube_meta,
            spec=V1DeploymentSpec(
                replicas=self.replicas,
                selector=self.to_kube_select(),
                template=self.template.to_kube()
            )
        )

    # def to_dict(self) -> dict:
    #     d = super().to_dict()
    #     # d['apiVersion'] = d.pop('api_version', None)
    #     return d

    def override_name(self, name: str):
        # logger.warning("FUN")
        self.add_name(name)
        self.template.override_name(name)

    def override_image(self, img: str):
        self.template.override_image(img)

    def override_port(self, num: int):
        for conts in self.template.pod_spec.containers:
            conts.ports = [num]
        # self.template.pod_spec.containers = [ct.ports = [num] for ct in conts]
