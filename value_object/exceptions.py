import typing


class MissingAttribute(Exception):
    def __init__(self, class_instance, key: str):
        klass = class_instance.__class__
        super(MissingAttribute, self).__init__(
            'On {}: Missing attribute `{}`.'.format(
                klass.__name__, key
            )
        )


class InvalidAttribute(Exception):
    def __init__(self, class_instance, key: str, value: typing.Any):
        klass = class_instance.__class__
        super(InvalidAttribute, self).__init__(
            'On {}: Invalid attribute `{}`, got {} which is a {}.'.format(
                klass.__name__, key, value, type(value)
            )
        )
