import abc
import inspect
from abc import ABCMeta
from typing import Any, Dict, Set

import addict as ad
from decopatch import function_decorator
from inflection import underscore
from loguru import logger
from pydantic import BaseModel, Field
from toolz import curry
from contextlib import suppress

SKIP_MEMBERS = [
    'Config',
    '__abstractmethods__',
    '__annotations__',
    '__class__',
    '__config__',
    '__custom_root_type__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__fields__',
    '__fields_set__',
    '__format__',
    '__ge__',
    '__get_validators__',
    '__getattribute__',
    '__getstate__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__iter__',
    '__json_encoder__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__post_root_validators__',
    '__pre_root_validators__',
    '__pretty__',
    '__private_attributes__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__repr_args__',
    '__repr_name__',
    '__repr_str__',
    '__schema_cache__',
    '__setattr__',
    '__setstate__',
    '__signature__',
    '__sizeof__',
    '__slots__',
    '__str__',
    '__subclasshook__',
    '__validators__',
    '__values__',
    '_abc_impl',
    '_calculate_keys',
    '_decompose_class',
    '_get_value',
    '_init_private_attributes',
    '_iter',
    'construct',
    'copy',
    'dict',
    'fields',
    'from_orm',
    'json',
    'parse_file',
    'parse_obj',
    'parse_raw',
    'schema',
    'schema_json',
    'to_string',
    'update_forward_refs',
    'validate'
]

EXISTING_FUNCS: Set[str] = set()
