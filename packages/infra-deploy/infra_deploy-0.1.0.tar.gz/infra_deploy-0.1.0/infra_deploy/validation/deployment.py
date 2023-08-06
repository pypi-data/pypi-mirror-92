from copy import copy, deepcopy
import typing
from pydantic import validate_arguments
from infra_deploy.models.container import ContainerModel
from infra_deploy.models.enums import SpecTypes
from collections import Counter

SPEC_TYPE = typing.List['SpecTypes']


def is_specs(spec_list: SPEC_TYPE, required_specs: SPEC_TYPE) -> bool:
    if not required_specs: return True
    if not spec_list: return False

    spec_count = Counter(spec_list)
    req_count = Counter(required_specs)
    for k, v in req_count.items():
        if k not in spec_count: return False
        if v <= spec_count[k]: return False
    return True


@validate_arguments
def is_containers(containers: typing.List['ContainerModel']) -> bool:
    return len(containers) > 0