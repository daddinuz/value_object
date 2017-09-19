import typing
from pycomb import exceptions as pycomb_exceptions
from value_object import AbstractAttributeType


class GenericAttributeType(AbstractAttributeType):
    def __init__(self, trait: typing.Type):
        self._trait = trait

    @property
    def trait(self) -> typing.Type:
        return self._trait

    def is_valid(self, value: typing.Any) -> bool:
        return isinstance(value, self._trait)


class PyCombAttributeType(AbstractAttributeType):
    def __init__(self, trait: typing.Type, combinator: callable):
        self._trait = trait
        self._combinator = combinator

    @property
    def trait(self) -> typing.Type:
        return self._trait

    def is_valid(self, value: typing.Any) -> bool:
        try:
            self._combinator(value)
        except pycomb_exceptions.PyCombValidationError:
            return False
        return True
