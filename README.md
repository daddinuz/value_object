Value Object
============

[![Build Status](https://travis-ci.org/daddinuz/value_object.svg?branch=master)](https://travis-ci.org/daddinuz/value_object)

```python
from value_object import ValueObject, Attribute


class Point(ValueObject):
    x = Attribute(int, float)
    y = Attribute(int, float)

# Valid use
point1 = Point(x=1, y=1)
point2 = Point(x=2, y=2)
point2.x - point1.x  # outputs 1
point2.y - point1.y  # outputs 1

# Invalid use:
Point(x=3)  # raises MissingAttribute
```

## CREDITS

Thanks to [pycomb](https://github.com/fcracker79/pycomb)!
