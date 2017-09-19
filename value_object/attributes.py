import typing
import itertools
from value_object import AbstractAttribute, AbstractAttributeType
from value_object.attribute_types import GenericAttributeType


class Attribute(AbstractAttribute):
    def __init__(self, *types: AbstractAttributeType):
        assert types and all(isinstance(t, AbstractAttributeType) for t in types)
        self._types = types

    @property
    def traits(self) -> typing.Sequence[typing.Type]:
        return [t.trait for t in self._types]

    @property
    def types(self) -> typing.Sequence[AbstractAttributeType]:
        return self._types

    def is_valid(self, value: typing.Any) -> bool:
        return any(x.is_valid(value) for x in self._types)


def of(*traits: typing.Type, nullable: bool = False) -> AbstractAttribute:
    return Attribute(
        *itertools.chain(
            (GenericAttributeType(t) for t in traits),
            (GenericAttributeType(type(None)),) if nullable else ())
    )
