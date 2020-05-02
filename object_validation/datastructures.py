import typing


ERRORS_TYPE = typing.Dict[str, str]

class ValidationResult:
    def __init__(self, value: typing.Any, errors: ERRORS_TYPE = None) -> None:
        self.value = value
        if errors is not None:
            self.errors = errors

    def has_error(self) -> bool:
        return hasattr(self, 'errors')

    def get_errors(self) -> ERRORS_TYPE:
        return getattr(self, 'errors', None)