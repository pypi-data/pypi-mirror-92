"""
Creates, updates, and deletes a deployment using AppsV1Api.
"""

import abc
from typing import Any, Dict, Optional, TypedDict, Union
from pydantic import BaseModel
from inflection import camelize
from infra_deploy import (
    utils,
    PropertyBaseModel,
)
DictAny = Dict[Any, Any]
DictStrAny = Dict[str, Any]
RecurseDictAny = Dict[str, DictStrAny]

ODStr = Optional[DictStrAny]
ODRecurse = Optional[RecurseDictAny]
DictUnion = Union[ODRecurse, ODStr]
DictUnionAny = Union[ODRecurse, ODStr, DictAny]


class LabelSelect(PropertyBaseModel):
    labels: DictUnion
    matchLabels: DictUnion
    nodeSelector: DictUnion

    class Config:
        extra = "allow"

    def __init__(
        __py_self__,
        labels: DictUnionAny = {},
        match_labels: DictUnionAny = {},
        node_selector: DictUnionAny = {},
        **data: Any
    ) -> None:

        super().__init__(**data)

        if labels:
            __py_self__.labels = labels
        if match_labels:
            __py_self__.match_labels = match_labels
        if node_selector:
            __py_self__.node_selector = node_selector

    def add(self, name, value):
        setattr(self, name, value)
        # self[name] = value

    def to_kube(self):
        all_items = self.dict()
        return utils.remove_nones_dict({
            camelize(k): v
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
