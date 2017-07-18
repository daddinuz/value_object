import unittest
from value_object import ValueObject, Attribute, exceptions


class Person(ValueObject):
    first_name = Attribute(str)
    last_name = Attribute(str)
    age = Attribute(int)


class TestPerson(unittest.TestCase):
    def test_signature(self):
        EXPECTED_ATTRIBUTES = dict(first_name=(str,), last_name=(str,), age=(int,))
        FIRST_NAME, LAST_NAME, AGE = 'Mario', 'Rossi', 38

        with self.assertRaises(AssertionError) as e:
            Person(
                {'first_name': FIRST_NAME, 'last_name': LAST_NAME, 'age': AGE},
                first_name=FIRST_NAME,
                last_name=LAST_NAME,
                age=AGE,
            )
        self.assertEqual('Must specify input_dict or entries, both are not allowed', str(e.exception))

        with self.assertRaises(exceptions.MissingAttribute) as e:
            Person(
                first_name=FIRST_NAME,
                last_name=LAST_NAME
            )
        self.assertEqual('On Person: Missing attribute `age`.', str(e.exception))

        with self.assertRaises(exceptions.InvalidAttribute) as e:
            Person(
                first_name=FIRST_NAME,
                last_name=AGE,
                age=AGE
            )
        self.assertEqual(
            "On Person: invalid attribute `last_name`, expected an instance of (<class 'str'>,), got 38 which is a <class 'int'>.",
            str(e.exception)
        )

        sut = Person(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            age=AGE,
        )
        self.assertEqual(FIRST_NAME, sut.first_name)
        self.assertEqual(LAST_NAME, sut.last_name)
        self.assertEqual(AGE, sut.age)
        self.assertIsInstance(sut._attributes, dict)
        self.assertEqual(EXPECTED_ATTRIBUTES, sut._attributes)

        with self.assertRaises(exceptions.InvalidAttribute) as e:
            sut.age = float(AGE)
        self.assertEqual(
            "On Person: invalid attribute `age`, expected an instance of (<class 'int'>,), got 38.0 which is a <class 'float'>.",
            str(e.exception)
        )


class Pet(ValueObject):
    name = Attribute(str)
    owner = Attribute(Person, nullable=True)


class TestPet(unittest.TestCase):
    def setUp(self):
        FIRST_NAME, LAST_NAME, AGE = 'Mario', 'Rossi', 38

        self.person = Person(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            age=AGE
        )

    def test_signature(self):
        EXPECTED_ATTRIBUTES = dict(name=(str,), owner=(Person, type(None)))
        NAME, OWNER = 'Garfield', self.person

        with self.assertRaises(AssertionError) as e:
            Pet(
                {'name': NAME, 'owner': OWNER},
                name=NAME,
                owner=OWNER,
            )
        self.assertEqual('Must specify input_dict or entries, both are not allowed', str(e.exception))

        with self.assertRaises(exceptions.MissingAttribute) as e:
            Pet()
        self.assertEqual('On Pet: Missing attribute `name`.', str(e.exception))

        with self.assertRaises(exceptions.InvalidAttribute) as e:
            Pet(
                name=NAME,
                owner=self.person.first_name
            )
        self.assertEqual(
            "On Pet: invalid attribute `owner`, expected an instance of (<class 'value_object.test.test_value_object.Person'>, <class 'NoneType'>), got Mario which is a <class 'str'>.",
            str(e.exception)
        )

        sut = Pet(
            name=NAME
        )

        self.assertEqual(NAME, sut.name)
        self.assertEqual(None, sut.owner)
        self.assertIsInstance(sut._attributes, dict)
        self.assertEqual(EXPECTED_ATTRIBUTES, sut._attributes)

        sut = Pet(
            name=NAME,
            owner=OWNER
        )

        self.assertEqual(NAME, sut.name)
        self.assertEqual(OWNER, sut.owner)
        self.assertIsInstance(sut._attributes, dict)
        self.assertEqual(EXPECTED_ATTRIBUTES, sut._attributes)

        sut.owner = None
        self.assertEqual(None, sut.owner)

        with self.assertRaises(exceptions.InvalidAttribute) as e:
            sut.owner = self.person.first_name
        self.assertEqual(
            "On Pet: invalid attribute `owner`, expected an instance of (<class 'value_object.test.test_value_object.Person'>, <class 'NoneType'>), got Mario which is a <class 'str'>.",
            str(e.exception)
        )


class Point(ValueObject):
    x = Attribute(int, float)
    y = Attribute(int, float)


class TestPoint(unittest.TestCase):
    def test_signature(self):
        EXPECTED_ATTRIBUTES = dict(x=(int, float), y=(int, float))
        X1, Y1 = 0, 0
        X2, Y2 = 1.2, 3.5

        with self.assertRaises(AssertionError) as e:
            Point(
                {'x': X1, 'y': Y1},
                x=X1,
                y=Y1,
            )
        self.assertEqual('Must specify input_dict or entries, both are not allowed', str(e.exception))

        with self.assertRaises(exceptions.MissingAttribute) as e:
            Point(
                x=X1,
            )
        self.assertEqual('On Point: Missing attribute `y`.', str(e.exception))

        with self.assertRaises(exceptions.InvalidAttribute) as e:
            Point(
                x=str(X1),
                y=Y1
            )
        self.assertEqual(
            "On Point: invalid attribute `x`, expected an instance of (<class 'int'>, <class 'float'>), got 0 which is a <class 'str'>.",
            str(e.exception)
        )

        sut = Point(
            x=X1,
            y=Y1,
        )
        self.assertEqual(X1, sut.x)
        self.assertEqual(Y1, sut.y)
        self.assertIsInstance(sut._attributes, dict)
        self.assertEqual(EXPECTED_ATTRIBUTES, sut._attributes)

        with self.assertRaises(exceptions.InvalidAttribute) as e:
            sut.y = str(Y1)
        self.assertEqual(
            "On Point: invalid attribute `y`, expected an instance of (<class 'int'>, <class 'float'>), got 0 which is a <class 'str'>.",
            str(e.exception)
        )

        sut = Point(
            x=X2,
            y=Y2,
        )
        self.assertEqual(X2, sut.x)
        self.assertEqual(Y2, sut.y)
        self.assertIsInstance(sut._attributes, dict)
        self.assertEqual(EXPECTED_ATTRIBUTES, sut._attributes)

        with self.assertRaises(exceptions.InvalidAttribute) as e:
            sut.x = str(Y2)
        self.assertEqual(
            "On Point: invalid attribute `x`, expected an instance of (<class 'int'>, <class 'float'>), got 3.5 which is a <class 'str'>.",
            str(e.exception)
        )


class Mixin(ValueObject):
    value = Attribute()


class TestMixin(unittest.TestCase):
    def test_signature(self):
        EXPECTED_ATTRIBUTES = dict(value=tuple())

        with self.assertRaises(AssertionError) as e:
            Mixin(
                {'value': 'foo'},
                value='foo',
            )
        self.assertEqual('Must specify input_dict or entries, both are not allowed', str(e.exception))

        with self.assertRaises(exceptions.MissingAttribute) as e:
            Mixin(foo='bar')
        self.assertEqual('On Mixin: Missing attribute `value`.', str(e.exception))

        sut = Mixin(
            value='foo'
        )
        self.assertEqual('foo', sut.value)
        self.assertIsInstance(sut._attributes, dict)
        self.assertEqual(EXPECTED_ATTRIBUTES, sut._attributes)

        sut = Mixin(
            value=5
        )
        self.assertEqual(5, sut.value)
        self.assertIsInstance(sut._attributes, dict)
        self.assertEqual(EXPECTED_ATTRIBUTES, sut._attributes)

        sut = Mixin(
            value=[1, 2, 3]
        )
        self.assertEqual([1, 2, 3], sut.value)
        self.assertIsInstance(sut._attributes, dict)
        self.assertEqual(EXPECTED_ATTRIBUTES, sut._attributes)
