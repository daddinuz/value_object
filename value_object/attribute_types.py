import enum
import typing
from pycomb import exceptions as pycomb_exceptions

from value_object import AbstractAttributeType, ValueObject


class BuiltinAttributeType(AbstractAttributeType):
    _BUILTIN_TYPES = (
        type, type(None), bool, int, float, complex, str, bytes, tuple, list, set, frozenset, dict, enum.Enum
    )

    def __init__(self, kind: typing.Type):
        if kind not in self._BUILTIN_TYPES:
            raise ValueError(
                'Kind must be one of {}, got: {} which is of type: {}'.format(
                    self._BUILTIN_TYPES, kind, type(kind)
                )
            )
        self._kind = kind

    def is_valid(self, value: typing.Any) -> bool:
        # noinspection PyBroadException
        try:
            return isinstance(value, self._kind)
        except:
            return False


class ValueObjectAttributeType(AbstractAttributeType):
    def __init__(self, obj: typing.Type[ValueObject]):
        self._obj = obj

    def is_valid(self, value: typing.Any) -> bool:
        # noinspection PyBroadException
        try:
            return type(value) == self._obj
        except:
            return False


class PyCombAttributeType(AbstractAttributeType):
    def __init__(self, combinator: callable):
        self._combinator = combinator

    def is_valid(self, value: typing.Any) -> bool:
        try:
            self._combinator(value)
        except pycomb_exceptions.PyCombValidationError:
            return False
        return True
