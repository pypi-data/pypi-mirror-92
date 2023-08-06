"""
Creates, updates, and deletes a deployment using AppsV1Api.
"""

import abc
from typing import Any, Dict, Optional, Union
from inflection import camelize
from infra_deploy import (
    utils,
    PropertyBaseModel,
)
from kubernetes import client as kli
# from kubernetes.client import V1LabelSelector
DictAny = Dict[Any, Any]
DictStrAny = Dict[str, Any]
RecurseDictAny = Dict[str, DictStrAny]

ODStr = Optional[DictStrAny]
ODRecurse = Optional[RecurseDictAny]
DictUnion = Union[ODRecurse, ODStr]
DictUnionAny = Union[ODRecurse, ODStr, DictAny]
METADATA_ATTR_MAP = kli.V1ObjectMeta.attribute_map


class LabelSelect(PropertyBaseModel):
    labels: DictUnion
    matchLabels: DictUnion
    nodeSelector: DictUnion

    class Config:
        extra = "allow"

    def __init__(
        self,
        labels: DictUnionAny = {},
        match_labels: DictUnionAny = {},
        node_selector: DictUnionAny = {},
        **data: Any
    ) -> None:

        super().__init__(**data)

        if labels:
            self.labels = labels
        if match_labels:
            self.match_labels = match_labels
        if node_selector:
            self.node_selector = node_selector

    def add(self, name, value):
        setattr(self, name, value)

    def to_kube(self) -> Dict:
        all_items = self.dict()
        return utils.remove_nones_dict({
            camelize(k,
                     False): v
            for k,
            v in all_items.items()
        })


class Selectable(PropertyBaseModel, abc.ABC):
    selector: LabelSelect = LabelSelect()    # type: ignore

    def add_selector(self, name: str, value: Any):
        """Add a selector value. Can use to instantly add selector attributes to the codebase.

        Args:
            name (str): The name of the selector
            value (Any): The value of a selector. Usually it's a dict, leaving it as any until we have a definition defined.
        """
        self.__add_selector_behavior(name, value)

    def __add_selector_behavior(self, name: str, value: Any):
        self.selector.add(name, value)

    def to_kube_select(self):
        return self.selector.to_kube()


class Metadatable(PropertyBaseModel, abc.ABC):
    metadata: DictStrAny = {}

    def add_meta(self, name: str, value: Any):
        if name not in METADATA_ATTR_MAP:
            # We're not adding anything in at this point
            return
        self.metadata[name] = value

    @property
    def kube_meta(self) -> kli.V1ObjectMeta:
        # NOTE: IRL will memoize the data in here using constant
        _metadata = utils.rip_meta(self.metadata)
        return kli.V1ObjectMeta(**_metadata)

    @property
    def kstep(self) -> DictStrAny:
        # NOTE: IRL will memoize the data in here using constant

        return self.kube_meta.to_dict()