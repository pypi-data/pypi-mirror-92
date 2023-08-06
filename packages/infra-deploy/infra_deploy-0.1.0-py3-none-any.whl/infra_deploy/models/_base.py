import abc
from infra_deploy import utils
from typing import Any, Dict, AnyStr, Union

from infra_deploy.constants import (
    ROOT_VALIDATOR_CONFIG_KEY,
    TEST_ROOT_CONFIG_KEY,
    VALIDATOR_CONFIG_KEY
)
from kubernetes import client as kli
from pydantic import BaseModel

# from infra_deploy.decorators import gather_all_validators
# from pydantic.main import ModelMetaclass

DictStrAny = Dict[str, Any]
RecurseDictAny = Dict[str, DictStrAny]


class GeneralAPI(BaseModel, abc.ABC):
    @abc.abstractmethod
    def to_kube(
        self
    ) -> Union[kli.V1Deployment,
               kli.CoreApi,
               kli.CoreV1Api,
               kli.CustomObjectsApi]:
        raise NotImplementedError

    def config_dict(self) -> Dict[AnyStr, AnyStr]:
        return utils.remove_nones_dict(self.to_kube().to_dict())

    @abc.abstractmethod
    def to_dict(self) -> Dict[AnyStr, AnyStr]:
        raise NotImplementedError("To dict is not implemented.")