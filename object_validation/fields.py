from decimal import Decimal
from object_validation.exceptions import ValidationError
import typing
from abc import abstractmethod

from object_validation.datastructures import ValidationResult

if typing.TYPE_CHECKING:
    from object_validation.models import Model


NO_DEFAULT = object()


class ModelField:
    def __init__(self, default: typing.Any = NO_DEFAULT, nullable: bool = True):
        if default is NO_DEFAULT and nullable:
            default = None

        if default is not NO_DEFAULT:
            self.default = default

        self.nullable = nullable

    @abstractmethod
    def validate(self, value: typing.Any) -> ValidationResult:
        pass

    def has_default(self) -> bool:
        return hasattr(self, 'default')

    def get_default_value(self) -> typing.Any:
        default = getattr(self, 'default', None)
        if callable(default):
            return default()
        return default


class Integer(ModelField):
    def __init__(self, **kwargs: typing.Dict[str, typing.Any]) -> None:
        super().__init__(**kwargs) # type: ignore

    def validate(self, value: typing.Any) -> ValidationResult:
        if value is None and self.nullable:
            return ValidationResult(
                value
            )

        errors = None
        if (
            isinstance(value, int) or
            isinstance(value, float) or
            isinstance(value, str) or
            isinstance(value, Decimal)
        ):
            try:
                value = int(value)
            except ValueError:
                errors = {
                    'value_error': f'{value}'
                }
        else:
            errors = {
                'type': f'type `{type(value)}` not allowed'
            }
        return ValidationResult(
            value=value,
            errors=errors,
        )


class Reference(ModelField):
    def __init__(self, model: typing.Type['Model'], **kwargs: typing.Dict[str, typing.Any]) -> None:
        super().__init__(**kwargs) # type: ignore
        self.model = model

    def validate(self, value: typing.Dict[str, typing.Any]) -> ValidationResult:
        try:
            return ValidationResult(
                self.model(**value),
            )
        except ValidationError as err:
            return ValidationResult(
                value,
                err.errors,
            )