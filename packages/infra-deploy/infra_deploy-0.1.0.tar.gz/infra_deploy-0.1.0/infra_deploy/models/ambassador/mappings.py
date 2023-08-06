from __future__ import annotations

from loguru import logger
import yaml
from infra_deploy.base import PropertyBaseModel

import inspect
from enum import Enum
from typing import Any, AnyStr, Dict, List, Optional, Union

import addict as adt
from devtools import debug
from toolz import keyfilter
from infra_deploy.decorators import DictStrAny
from infra_deploy.metadata.decorators.attrs import metagroups
from infra_deploy.models.base import KubeModel
from infra_deploy.models.general import Metadatable
from infra_deploy.utils import remove_nones_dict as cleard
from kubernetes.client import V1ObjectMeta, V1Volume
from pydantic import BaseModel, Extra, root_validator
from pydantic.dataclasses import dataclass

DictStr = Dict[str, str]
OptDictStr = Optional[DictStr]
OptDictStrAny = Optional[DictStrAny]
OptStr = Optional[str]
OptInt = Optional[int]
OptBool = Optional[bool]


class ApiVersionNum(str, Enum):
    V2 = 'getambassador.io/v2'


class AmbassadorKinds(str, Enum):
    Project = 'Project'
    FilterPolicy = 'FilterPolicy'
    Mapping = "Mapping"
    Module = "Module"
    Filter = "Filter"


class MetadataLabels(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class Priority(str, Enum):
    DEFAULT = 'default'
    HIGH = 'high'


class CircuitBreaker(BaseModel):
    priority: Optional[Priority] = None
    max_connections: OptInt = None
    max_pending_requests: OptInt = None
    max_requests: OptInt = None
    max_retries: OptInt = None


class Cors(BaseModel):
    origins: Optional[Union[str, List[str]]] = None
    methods: Optional[Union[str, List[str]]] = None
    headers: Optional[Union[str, List[str]]] = None
    credentials: OptBool = None
    exposed_headers: Optional[Union[str, List[str]]] = None
    max_age: OptStr = None


class RetryOn(str, Enum):
    XX5 = '5xx'
    GATEWAY_ERROR = 'gateway-error'
    CONNECT_FAILURE = 'connect-failure'
    XX4 = 'retriable-4xx'
    REFUSED_STREAM = 'refused-stream'
    RETRIABLE_STATUS_CODES = 'retriable-status-codes'


class RetryPolicy(BaseModel):
    retry_on: Optional[RetryOn] = None
    num_retries: OptInt = None
    per_try_timeout: OptStr = None


class Policy(str, Enum):
    ROUND = 'round_robin'
    RING = 'ring_hash'
    MAG = 'maglev'
    LEAST = 'least_request'


class Cookie(BaseModel):
    name: str
    path: OptStr = None
    ttl: OptStr = None

    def __init__(
        self,
        *,
        name: str,
        path: OptStr,
        ttl: OptStr,
        **data: Any
    ) -> None:
        super().__init__(**data)


class LoadBalancer(BaseModel):
    policy: Policy
    cookie: Optional[Cookie] = None
    header: OptStr = None
    source_ip: OptBool = None


class RateLimit(BaseModel):
    __root__: Union[List[Any], Dict[str, Any]]


class MappingVars(KubeModel, Metadatable):
    __api_model__: V1Volume = V1Volume

    name: str
    prefix: str
    service: str

    kind: AmbassadorKinds = AmbassadorKinds.Mapping
    api_version: ApiVersionNum = ApiVersionNum.V2
    generation: OptInt = None
    namespace: OptStr = None
    ambassador_id: Optional[Union[str, List[str]]] = None
    prefix_regex: OptBool = None
    prefix_exact: OptBool = None
    add_request_headers: OptDictStrAny = None
    add_response_headers: OptDictStrAny = None
    add_linkerd_headers: OptBool = None
    auto_host_rewrite: OptBool = None
    case_sensitive: OptBool = None
    enable_ipv4: OptBool = None
    enable_ipv6: OptBool = None
    circuit_breakers: Optional[List[CircuitBreaker]] = None
    cors: Optional[Cors] = None
    retry_policy: Optional[RetryPolicy] = None
    grpc: OptBool = None
    host_redirect: OptBool = None
    host_rewrite: OptStr = None
    method: OptStr = None
    method_regex: OptStr = None
    outlier_detection: OptStr = None
    path_redirect: OptStr = None
    priority: OptStr = None
    precedence: OptStr = None
    cluster_tag: OptStr = None
    remove_request_headers: Optional[Union[str, List[str]]] = None
    remove_response_headers: Optional[Union[str, List[str]]] = None
    resolver: OptStr = None
    rewrite: OptStr = None
    regex_rewrite: Optional[Dict[str, str]] = None
    shadow: OptBool = None
    connect_timeout_ms: OptInt = None
    cluster_idle_timeout_ms: OptInt = None
    timeout_ms: OptInt = None
    idle_timeout_ms: OptInt = None
    tls: Optional[Union[str, bool]] = None
    use_websocket: OptBool = None
    allow_upgrade: Optional[List[str]] = None
    weight: OptInt = None
    bypass_auth: OptBool = None
    modules: Optional[List[Dict[str, Any]]] = None
    host: OptStr = None
    host_regex: OptBool = None
    headers: OptDictStr = None
    regex_headers: OptDictStr = None
    labels: OptDictStrAny = None
    envoy_override: OptDictStrAny = None
    load_balancer: OptDictStr = None
    query_parameters: OptDictStr = None
    regex_query_parameters: OptDictStr = None

    def key_filtred_attrs(self, _keys: List[str]) -> DictStrAny:
        fld = self.dict()
        # logger.info("Trying to extract ambassador")
        ext_items = cleard(keyfilter(lambda x: x in _keys, fld))
        return ext_items


class MappingSpec(PropertyBaseModel):
    prefix: str
    service: str
    config: DictStrAny = {}
    retry_policy: Optional[RetryPolicy] = None
    method: OptStr = None
    connect_timeout_ms: OptInt = None
    cluster_idle_timeout_ms: OptInt = None
    timeout_ms: OptInt = None
    idle_timeout_ms: OptInt = None

    @root_validator
    def required_rearrangements(cls, values):
        addictified = adt.Dict(**values)
        if not addictified.retry_policy:
            # Should return a {} if it's empty and just return the value
            return values
        typed_retry: RetryPolicy = addictified.retry_policy
        addictified.config.retry_policy = typed_retry.dict()
        return addictified

    def field_keys(self) -> List[str]:
        print("Checking here")
        resp = list(self.dict().keys())
        return resp

    # add_linkerd_headers
    # allow_request_body
    # allowed_authorization_headers
    # allowed_request_headers
    # ambassador_id
    # auth_service
    # failure_mode_allow
    # path_prefix
    # include_body
    # protocol_version
    # status_on_error
    # tls


class AMExporter(BaseModel):
    class Config:
        extra = "allow"
        use_enum_values = True

    apiVersion: ApiVersionNum = ApiVersionNum.V2
    kind: AmbassadorKinds = AmbassadorKinds.Mapping
    metadata: DictStrAny
    spec: MappingSpec

    def dict(self, *args, **kwargs) -> 'DictStrAny':
        return cleard(super().dict(*args, **kwargs))


class Mapping(MappingVars):
    def __init__(
        self,
        *,
        name: str,
        prefix: str,
        service: str,
        kind: AmbassadorKinds = AmbassadorKinds.Mapping,
        api_version: ApiVersionNum = ApiVersionNum.V2,
        namespace: OptStr = None,
        generation: OptInt = None,
        metadata_labels: Optional[Dict[str,
                                       MetadataLabels]] = None,
        ambassador_id: Optional[Union[str,
                                      List[str]]] = None,
        prefix_regex: OptBool = None,
        prefix_exact: OptBool = None,
        add_request_headers: OptDictStrAny = None,
        add_response_headers: OptDictStrAny = None,
        add_linkerd_headers: OptBool = None,
        auto_host_rewrite: OptBool = None,
        case_sensitive: OptBool = None,
        enable_ipv4: OptBool = None,
        enable_ipv6: OptBool = None,
        circuit_breakers: Optional[List[CircuitBreaker]] = None,
        cors: Optional[Cors] = None,
        retry_policy: Optional[RetryPolicy] = None,
        grpc: OptBool = None,
        host_redirect: OptBool = None,
        host_rewrite: OptStr = None,
        method: OptStr = None,
        method_regex: OptBool = None,
        outlier_detection: OptStr = None,
        path_redirect: OptStr = None,
        priority: OptStr = None,
        precedence: OptInt = None,
        cluster_tag: OptStr = None,
        remove_request_headers: Optional[Union[str,
                                               List[str]]] = None,
        remove_response_headers: Optional[Union[str,
                                                List[str]]] = None,
        resolver: OptStr = None,
        rewrite: OptStr = None,
        regex_rewrite: Optional[Dict[str,
                                     str]] = None,
        shadow: OptBool = None,
        connect_timeout_ms: OptInt = None,
        cluster_idle_timeout_ms: OptInt = None,
        timeout_ms: OptInt = None,
        idle_timeout_ms: OptInt = None,
        tls: Optional[Union[str,
                            bool]] = None,
        use_websocket: OptBool = None,
        allow_upgrade: Optional[List[str]] = None,
        weight: OptInt = None,
        bypass_auth: OptBool = None,
        modules: Optional[List[Dict[str,
                                    Any]]] = None,
        host: OptStr = None,
        host_regex: OptBool = None,
        headers: OptDictStr = None,
        regex_headers: OptDictStr = None,
        labels: Optional[Dict[str,
                              Any]] = None,
        envoy_override: Optional[Dict[str,
                                      Any]] = None,
        load_balancer: OptDictStr = None,
        query_parameters: OptDictStr = None,
        regex_query_parameters: OptDictStr = None,
        **data: Any
    ) -> None:

        non_null = cleard(
            dict(
                kind=kind,
                name=name,
                prefix=prefix,
                service=service,
                api_version=api_version,
                generation=generation,
                namespace=namespace,
                metadata_labels=metadata_labels,
                ambassador_id=ambassador_id,
                prefix_regex=prefix_regex,
                prefix_exact=prefix_exact,
                add_request_headers=add_request_headers,
                add_response_headers=add_response_headers,
                add_linkerd_headers=add_linkerd_headers,
                auto_host_rewrite=auto_host_rewrite,
                case_sensitive=case_sensitive,
                enable_ipv4=enable_ipv4,
                enable_ipv6=enable_ipv6,
                circuit_breakers=circuit_breakers,
                cors=cors,
                retry_policy=retry_policy,
                grpc=grpc,
                host_redirect=host_redirect,
                host_rewrite=host_rewrite,
                method=method,
                method_regex=method_regex,
                outlier_detection=outlier_detection,
                path_redirect=path_redirect,
                priority=priority,
                precedence=precedence,
                cluster_tag=cluster_tag,
                remove_request_headers=remove_request_headers,
                remove_response_headers=remove_response_headers,
                resolver=resolver,
                rewrite=rewrite,
                regex_rewrite=regex_rewrite,
                shadow=shadow,
                connect_timeout_ms=connect_timeout_ms,
                cluster_idle_timeout_ms=cluster_idle_timeout_ms,
                timeout_ms=timeout_ms,
                idle_timeout_ms=idle_timeout_ms,
                tls=tls,
                use_websocket=use_websocket,
                allow_upgrade=allow_upgrade,
                weight=weight,
                bypass_auth=bypass_auth,
                modules=modules,
                host=host,
                host_regex=host_regex,
                headers=headers,
                regex_headers=regex_headers,
                labels=labels,
                envoy_override=envoy_override,
                load_balancer=load_balancer,
                query_parameters=query_parameters,
                regex_query_parameters=regex_query_parameters,
            )
        )
        data.update(non_null)
        super().__init__(**data)
        self.add_meta("name", name)

    def to_kube(self) -> DictStrAny:
        _map_spec_keys = list(MappingSpec.__fields__.keys())
        map_spec_attrs = self.key_filtred_attrs(_map_spec_keys)
        if self.namespace:
            ns: str = self.namespace
            srv: str = self.service
            map_spec_attrs["service"] = f"{srv}.{ns}"
            # del map_spec_attrs['namespace']
        exporter = AMExporter(
            metadata=self.kstep,
            spec=MappingSpec(**map_spec_attrs)
        )

        return exporter.dict()

    def dict(self, *args, **kwargs) -> 'DictStrAny':
        return cleard(super().dict(*args, **kwargs))

    def config_dict(self) -> Dict[AnyStr, AnyStr]:
        return self.to_kube()    # type: ignore

    def to_yaml(self) -> str:
        return yaml.dump(self.to_kube())


@metagroups(name="cors")
def create_mapping():
    return Mapping(
        name="sample-service",
        prefix="/",
        service="service.name",
        namespace="derpman_boogy"
    )


if __name__ == "__main__":
    ammap = Mapping(
        name="sample-service",
        prefix="/",
        service="service",
        namespace="derpman_boogidy"
    )

    print()
    logger.success(f"\n\n{ammap.to_yaml()}")
    print("\n")
