import typing


class ValidationError(Exception):
    def __init__(
        self,
        *,
        errors: typing.Dict[str, str]
    ) -> None:
        self.errors = errors
