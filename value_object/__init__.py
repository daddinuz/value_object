import typing
from value_object import exceptions


def _extract_classes(klass: typing.Type) -> typing.Set[typing.Type]:
    extracted = {klass}
    for base in klass.__bases__:
        extracted |= _extract_classes(base)

    if object in extracted:
        extracted.remove(object)

    return extracted


class ValueObject:
    """

    Declare a subclass with some attributes:

        class Point(ValueObject):
            x = Attribute(int, float)
            y = Attribute(int, float)

    Valid use:

        point1 = Point(x=1, y=1)
        point2 = Point(x=2, y=2)
        point2.x - point1.x # outputs 1
        point2.y - point1.y # outputs 1

    Invalid use:

        Point(x=3) # raises MissingAttribute

    """

    def __init__(self, input_dict: typing.Dict or None = None, **entries):
        assert not (input_dict and entries), 'Must specify input_dict or entries, both are not allowed'
        klass = self.__class__
        klass._attributes = {
            k: v.required_types
            for klass in _extract_classes(klass)
            for k, v in klass.__dict__.items()
            if isinstance(v, Attribute)
        }

        self.__dict__.update(input_dict or entries)
        for key, required_types in klass._attributes.items():
            if key not in self.__dict__:
                if type(None) in required_types:
                    self.__dict__[key] = None
                else:
                    raise exceptions.MissingAttribute(self, key)

            self._check_for_invalid_attribute(key, self.__dict__[key], required_types)

    def _check_for_invalid_attribute(self, key: str, value: typing.Any, required_types: typing.Tuple[typing.Type, ...]):
        if required_types and not isinstance(value, required_types):
            raise exceptions.InvalidAttribute(self, key, value)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setattr__(self, key, value):
        klass = self.__class__
        self._check_for_invalid_attribute(key, value, klass._attributes[key])
        super().__setattr__(key, value)


class Attribute:
    def __init__(self, *required_types: typing.Iterable[typing.Type], nullable: bool = False):
        if required_types and nullable:
            self._required_types = tuple(x for x in (*required_types, type(None)))
        else:
            self._required_types = tuple(x for x in required_types)

    @property
    def required_types(self) -> typing.Tuple[typing.Type, ...]:
        return self._required_types


# limit exported symbols
__all__ = ['ValueObject', 'Attribute']
