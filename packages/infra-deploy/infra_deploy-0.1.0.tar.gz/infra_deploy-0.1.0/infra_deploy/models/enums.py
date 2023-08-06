from auto_all import start_all, end_all
from enum import Enum

start_all(globals())


class SpecTypes(str, Enum):
    DEPLOY = "deployment"
    POD = "pod"
    POD_TEMPLATE = "pod_template"

    def named(self, name: str) -> str:
        return f"{self.value}_{name}"


class PullPolicy(str, Enum):
    ALWAYS = "Always"
    IF_PRESENT = "IfNotPresent"
    NEVER = "Never"

    def named(self, name: str) -> str:
        return f"{self.value}_{name}"


class ResourceTypes(str, Enum):
    LIMITS = "limits"
    REQUESTS = "requests"


class ServiceApiVersion(str, Enum):
    V1 = "v1"
    BETA = "v1beta1"


class ApiKinds(str, Enum):
    POD = "Pod"
    REP_CTL = "ReplicationController"
    SERVICE = "Service"
    NAMESPACE = "Namespace"
    NODE = "Node"


end_all(globals())