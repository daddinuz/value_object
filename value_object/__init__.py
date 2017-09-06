import abc
import typing

from value_object import exceptions


def _extract_classes(klass: typing.Type) -> typing.Set[typing.Type]:
    extracted = {klass}
    for base in klass.__bases__:
        extracted |= _extract_classes(base)
    if object in extracted:
        extracted.remove(object)
    return extracted


class AbstractAttributeType(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_valid(self, value: typing.Any) -> bool:
        pass  # pragma: no cover


class AbstractAttribute(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_valid(self, value: typing.Any) -> bool:
        pass  # pragma: no cover


class AbstractAttributeTypesFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def from_builtin_type(self, kind: typing.Type) -> AbstractAttributeType:
        pass  # pragma: no cover

    @abc.abstractmethod
    def from_value_object_type(self, obj: 'ValueObject') -> AbstractAttributeType:
        pass  # pragma: no cover

    @abc.abstractmethod
    def from_pycomb_combinator_type(self, combinator: typing.Callable) -> AbstractAttributeType:
        pass  # pragma: no cover


class ValueObject:
    def __init__(self, input_dict: typing.Dict or None = None, **entries):
        assert not (input_dict and entries), 'Must specify input_dict or entries, both are not allowed'

        klass = self.__class__
        klass._attributes = {
            key: attribute
            for klass in _extract_classes(klass)
            for key, attribute in klass.__dict__.items()
            if isinstance(attribute, AbstractAttribute)
        }

        self.__dict__.update(input_dict or entries)
        for key, attribute in klass._attributes.items():
            if key not in self.__dict__:
                if attribute.is_valid(None):
                    self.__dict__[key] = None
                else:
                    raise exceptions.MissingAttribute(self, key)
            value = self.__dict__[key]
            if not attribute.is_valid(value):
                raise exceptions.InvalidAttribute(self, key, value)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setattr__(self, key, value):
        klass = self.__class__
        attribute = klass._attributes.get(key)
        if attribute and not attribute.is_valid(value):
            raise exceptions.InvalidAttribute(self, key, value)
        super().__setattr__(key, value)

    def __eq__(self, other):
        return type(self) == type(other) and \
               all(getattr(self, k) == getattr(other, k) for k in self.attributes.keys())

    @property
    def attributes(self) -> typing.Dict[str, AbstractAttribute]:
        klass = self.__class__
        return klass._attributes


class Attribute(AbstractAttribute):
    def __init__(self, *types: typing.Iterable[typing.Type], nullable: bool = False):
        assert types
        assert None not in types
        import warnings
        from value_object.attributes import AttributeOfTypes
        from value_object.attribute_types_factory import _INSTANCE
        warnings.warn('class `Attribute` is deprecated use `AttributeOfTypes` instead.', DeprecationWarning)
        attribute_types = [t for t in types]
        nullable and attribute_types.append(type(None))

        def _create():
            for t in attribute_types:
                if issubclass(t, ValueObject):
                    yield _INSTANCE.from_value_object_type(t)
                else:
                    yield _INSTANCE.from_builtin_type(t)

        self._delegate = AttributeOfTypes(*_create())

    def is_valid(self, value: typing.Any) -> bool:
        return self._delegate.is_valid(value)
