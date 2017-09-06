import unittest
from value_object import ValueObject, Attribute, exceptions


class Person(ValueObject):
    first_name = Attribute(str)
    last_name = Attribute(str)
    age = Attribute(int)


class TestPerson(unittest.TestCase):
    EXPECTED_ATTRIBUTES = dict(first_name=Person.first_name, last_name=Person.last_name, age=Person.age)
    FIRST_NAME, LAST_NAME, AGE = 'Mario', 'Rossi', 38

    def test_signature(self):
        with self.assertRaises(AssertionError) as e:
            Person(
                {'first_name': self.FIRST_NAME, 'last_name': self.LAST_NAME, 'age': self.AGE},
                first_name=self.FIRST_NAME,
                last_name=self.LAST_NAME,
                age=self.AGE,
            )
        self.assertEqual('Must specify input_dict or entries, both are not allowed', str(e.exception))

        with self.assertRaises(exceptions.MissingAttribute) as e:
            Person(
                first_name=self.FIRST_NAME,
                last_name=self.LAST_NAME
            )
        self.assertEqual('On Person: Missing attribute `age`.', str(e.exception))

        with self.assertRaises(exceptions.InvalidAttribute) as e:
            Person(
                first_name=self.FIRST_NAME,
                last_name=self.AGE,
                age=self.AGE
            )
        self.assertEqual(
            "On Person: Invalid attribute `last_name`, got 38 which is a <class 'int'>.",
            str(e.exception),

        )

        sut = Person(
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
            age=self.AGE,
        )
        self.assertEqual(self.FIRST_NAME, sut.first_name)
        self.assertEqual(self.LAST_NAME, sut.last_name)
        self.assertEqual(self.AGE, sut.age)
        self.assertIsInstance(sut.attributes, dict)
        self.assertEqual(self.EXPECTED_ATTRIBUTES, sut.attributes)

        with self.assertRaises(exceptions.InvalidAttribute) as e:
            sut.age = float(self.AGE)
        self.assertEqual(
            "On Person: Invalid attribute `age`, got 38.0 which is a <class 'float'>.",
            str(e.exception)
        )

    def test_eq(self):
        sut1 = Person(
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
            age=self.AGE,
        )
        sut2 = Person(
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
            age=self.AGE,
        )
        sut3 = Person(
            first_name=self.LAST_NAME,
            last_name=self.FIRST_NAME,
            age=self.AGE,
        )
        self.assertEqual(sut1, sut2)
        self.assertFalse(sut1 == sut3)
        self.assertFalse(sut2 == sut3)


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
        EXPECTED_ATTRIBUTES = dict(name=Pet.name, owner=Pet.owner)
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
            "On Pet: Invalid attribute `owner`, got Mario which is a <class 'str'>.",
            str(e.exception)
        )

        sut = Pet(
            name=NAME
        )

        self.assertEqual(NAME, sut.name)
        self.assertEqual(None, sut.owner)
        self.assertIsInstance(sut.attributes, dict)
        self.assertEqual(EXPECTED_ATTRIBUTES, sut.attributes)

        sut = Pet(
            name=NAME,
            owner=OWNER
        )

        self.assertEqual(NAME, sut.name)
        self.assertEqual(OWNER, sut.owner)
        self.assertIsInstance(sut.attributes, dict)
        self.assertEqual(EXPECTED_ATTRIBUTES, sut.attributes)

        sut.owner = None
        self.assertEqual(None, sut.owner)

        with self.assertRaises(exceptions.InvalidAttribute) as e:
            sut.owner = self.person.first_name
        self.assertEqual(
            "On Pet: Invalid attribute `owner`, got Mario which is a <class 'str'>.",
            str(e.exception)
        )


class Point(ValueObject):
    x = Attribute(int, float)
    y = Attribute(int, float)


class TestPoint(unittest.TestCase):
    def test_signature(self):
        EXPECTED_ATTRIBUTES = dict(x=Point.x, y=Point.y)
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
            "On Point: Invalid attribute `x`, got 0 which is a <class 'str'>.",
            str(e.exception)
        )

        sut = Point(
            x=X1,
            y=Y1,
        )
        self.assertEqual(X1, sut.x)
        self.assertEqual(Y1, sut.y)
        self.assertIsInstance(sut.attributes, dict)
        self.assertEqual(EXPECTED_ATTRIBUTES, sut.attributes)

        with self.assertRaises(exceptions.InvalidAttribute) as e:
            sut.y = str(Y1)
        self.assertEqual(
            "On Point: Invalid attribute `y`, got 0 which is a <class 'str'>.",
            str(e.exception)
        )

        sut = Point(
            x=X2,
            y=Y2,
        )
        self.assertEqual(X2, sut.x)
        self.assertEqual(Y2, sut.y)
        self.assertIsInstance(sut.attributes, dict)
        self.assertEqual(EXPECTED_ATTRIBUTES, sut.attributes)

        with self.assertRaises(exceptions.InvalidAttribute) as e:
            sut.x = str(Y2)
        self.assertEqual(
            "On Point: Invalid attribute `x`, got 3.5 which is a <class 'str'>.",
            str(e.exception)
        )
