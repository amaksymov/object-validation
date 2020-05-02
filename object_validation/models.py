from abc import ABCMeta
import typing

from object_validation.fields import ModelField
from object_validation.exceptions import ValidationError


class ModelMetaclass(ABCMeta):
    def __new__(
        cls: type,
        name: str,
        bases: typing.Sequence[type],
        attrs: dict,
    ) -> 'ModelMetaclass':
        fields: typing.Dict[str, ModelField] = {}
        for key, value in list(attrs.items()):
            if isinstance(value, ModelField):
                attrs.pop(key)
                fields[key] = value

        attrs["fields"] = dict(fields.items())

        new_type = super(ModelMetaclass, cls).__new__(  # type: ignore
            cls, name, bases, attrs
        )
        return new_type


class Model(metaclass=ModelMetaclass):
    fields: typing.Dict[str, ModelField] = {}

    def __init__(self, **kwargs: typing.Dict[str, typing.Any]) -> None:
        errors: typing.Dict[str, typing.Any] = {}
        for key, field in self.fields.items():
            if key in kwargs.keys():
                result = field.validate(kwargs[key])
                if result.has_error():
                    errors[key] = result.get_errors()
                setattr(self, key, result.value)
            elif field.has_default():
                setattr(self, key, field.get_default_value())

        if errors != {}:
            raise ValidationError(errors=errors)
