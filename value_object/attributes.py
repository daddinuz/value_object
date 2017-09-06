import typing

from value_object import AbstractAttribute, AbstractAttributeType


class AttributeOfTypes(AbstractAttribute):
    def __init__(self, *types: typing.Iterable[AbstractAttributeType]):
        assert types
        assert None not in types
        self._types = types

    def is_valid(self, value: typing.Any) -> bool:
        return any(x.is_valid(value) for x in self._types)
