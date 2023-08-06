import warnings
from typing import Any
from typing import Generator
from typing import Callable as TypingCallable
from typing import Dict, Optional, Set, Union, overload
from pydantic.types import OptionalInt
from pydantic.validators import constr_length_validator, str_validator
from infra_deploy.utils import update_not_none

AnyCallable = TypingCallable[..., Any]
CallableGenerator = Generator[AnyCallable, None, None]


class ApiVersion:
    min_length: OptionalInt = None
    max_length: OptionalInt = None

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        update_not_none(
            field_schema,
            type='string',
            writeOnly=True,
        )

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield cls.validate
        yield constr_length_validator

    @classmethod
    def validate(cls, value: Any) -> 'ApiVersion':
        if isinstance(value, cls):
            return value
        value = str_validator(value)

        return cls(value)

    def __init__(self, value: str):
        self._secret_value = value

    def __repr__(self) -> str:
        return f"ApiVersion('{self}')"

    def __str__(self) -> str:
        return '**********' if self._secret_value else ''

    def __eq__(self, other: Any) -> bool:
        return isinstance(other,
                          ApiVersion) and self.get_secret_value(
                          ) == other.get_secret_value()

    def __len__(self) -> int:
        return len(self._secret_value)

    def display(self) -> str:
        warnings.warn(
            '`secret_str.display()` is deprecated, use `str(secret_str)` instead',
            DeprecationWarning
        )
        return str(self)

    def get_secret_value(self) -> str:
        return self._secret_value

    def group(self):
        values = self._secret_value.split("/")
        return values[0]

    def version(self):
        values = self._secret_value.split("/")
        return values[1]
