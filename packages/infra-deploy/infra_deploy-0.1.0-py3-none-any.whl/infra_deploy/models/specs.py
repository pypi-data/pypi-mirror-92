from infra_deploy.models.container import ContainerModel, Container, MemCPU
from typing import Any, List, Optional
from kubernetes import client as kli
from infra_deploy.models.base import KubeBase

from infra_deploy.models.labels import DictStrAny, LabelSelect, Selectable
from infra_deploy.helpers import (
    built_test_pod_template,
    built_test_deploy_spec,
    built_test_pod,
    create_test_container,
)
from infra_deploy import utils
from inflection import camelize

METADATA_ATTR_MAP = kli.V1ObjectMeta.attribute_map


class BaseSpec(KubeBase):
    metadata: DictStrAny = {}


class SpecPod(BaseSpec, Selectable):
    __context__: str = "pod__spec"
    # __metadata__: DictStrAny = {}
    containers: List[Container] = []

    def to_kube(self) -> kli.V1DeploymentSpec:
        kontainers = self.containers or []
        pod = kli.V1PodSpec(containers=[x.to_kube() for x in kontainers])
        return pod

    def override_name(self, name: str):
        for container in self.containers:
            container.name = name


class SpecPodTemplate(BaseSpec, Selectable):
    __context__: str = "pod_spec_template"
    """
        >>> @meta(labels=dict(app="deployment"))
        >>> def main_template(self):
        >>>   return SpecPodTemplate(...)
    """
    # __kube_model__: kli.V1PodTemplateSpec
    pod_spec: SpecPod = SpecPod()

    # containers: List[Container] = []

    def __init__(
        __pydantic_self__,
        containers: List[Container] = [],
        **data: Any
    ) -> None:
        super().__init__(**data)
        __pydantic_self__.add_containers(containers)

    # Here we'd add the metadata in via a decorator.
    # The decorator would call this function to run after the function has run.

    def add_meta(self, name: str, value: Any):
        if name not in METADATA_ATTR_MAP:
            # We're not adding anything in at this point
            return
        self.metadata[name] = value

    # def add_selector(self, name: str, value: Any):
    #     """Add a selector value. Can use to instantly add selector attributes to the codebase.

    #     Args:
    #         name (str): The name of the selector
    #         value (Any): The value of a selector. Usually it's a dict, leaving it as any until we have a definition defined.
    #     """
    #     self.__add_selector_behavior(name, value)

    def override_name(self, name: str):
        self.add_meta("labels", dict(app=(str(name))))
        self.add_selector("app", dict(app=str(name)))
        self.pod_spec.override_name(name)

    @property
    def kube_meta(self) -> kli.V1ObjectMeta:
        # NOTE: IRL will memoize the data in here using constant
        _metadata = utils.rip_meta(self.metadata)
        return kli.V1ObjectMeta(**_metadata)

    @property
    def kontainers(self) -> List[kli.V1Container]:
        # NOTE: IRL will memoize the data in here using constant
        return [x.to_kube() for x in self.containers]

    @property
    def containers(self):
        return self.pod_spec.containers

    def add_containers(self, _containers: List[Container]):
        self.pod_spec.containers = _containers

    # NOTE: For the main app we'll be able to
    def to_kube(self) -> kli.V1PodTemplateSpec:
        # self.containers
        return kli.V1PodTemplateSpec(
            metadata=self.kube_meta,
            spec=kli.V1PodSpec(containers=self.kontainers)
        )

    def override_image(self, img: str):
        conts = self.pod_spec.containers
        isolated = conts[0]
        isolated.image = img
        self.pod_spec.containers = [isolated]


ang = dict(app="nginx")


class SpecDeploy(BaseSpec):
    __context__: str = "pod_deploy_spec"
    replicas: int = 3
    template: SpecPodTemplate
    selector: LabelSelect = LabelSelect()    # type: ignore

    def __init__(
        __pydantic_self__,
        template: SpecPodTemplate,
        replicas: int = 3,
        selector: Optional[LabelSelect] = None,
        **data: Any
    ) -> None:
        __pydantic_self__.replicas = replicas
        __pydantic_self__.template = template
        if selector:
            __pydantic_self__.selector = selector
        super().__init__(**data)

    def to_kube(self) -> kli.V1DeploymentSpec:
        deployment = kli.V1DeploymentSpec(
            replicas=self.replicas,
            template=self.template.to_kube(),
            selector=utils.remove_nones_dict(self.selector.dict())
        )
        return deployment