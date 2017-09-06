import typing

from value_object import AbstractAttributeType, AbstractAttributeTypesFactory, ValueObject
from value_object.attribute_types import BuiltinAttributeType, ValueObjectAttributeType, PyCombAttributeType


class AttributeTypesFactory(AbstractAttributeTypesFactory):
    @classmethod
    def from_builtin_type(cls, kind: typing.Type) -> AbstractAttributeType:
        return BuiltinAttributeType(kind)

    @classmethod
    def from_value_object_type(cls, obj: typing.Type[ValueObject]) -> AbstractAttributeType:
        return ValueObjectAttributeType(obj)

    @classmethod
    def from_pycomb_combinator_type(cls, combinator: typing.Callable) -> AbstractAttributeType:
        return PyCombAttributeType(combinator)


_INSTANCE = AttributeTypesFactory()
