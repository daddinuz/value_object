import unittest
from value_object import Attribute


class TestAttribute(unittest.TestCase):
    def test_attribute_without_types(self):
        sut = Attribute()
        self.assertIsInstance(sut.required_types, tuple)
        self.assertEqual(tuple(), sut.required_types)

    def test_attribute_with_one_non_nullable_type(self):
        expected = (str,)
        sut = Attribute(str)
        self.assertIsInstance(sut.required_types, tuple)
        self.assertEqual(expected, sut.required_types)

    def test_attribute_with_many_non_nullable_types(self):
        expected = (str, int, list)
        sut = Attribute(str, int, list)
        self.assertIsInstance(sut.required_types, tuple)
        self.assertEqual(expected, sut.required_types)

    def test_attribute_without_types_specifying_nullable(self):
        sut = Attribute(nullable=True)
        self.assertIsInstance(sut.required_types, tuple)
        self.assertEqual(tuple(), sut.required_types)

    def test_attribute_with_one_nullable_type(self):
        expected = (str, type(None))
        sut = Attribute(str, nullable=True)
        self.assertIsInstance(sut.required_types, tuple)
        self.assertEqual(expected, sut.required_types)

    def test_attribute_with_many_nullable_types(self):
        expected = (int, float, type(None))
        sut = Attribute(int, float, nullable=True)
        self.assertIsInstance(sut.required_types, tuple)
        self.assertEqual(expected, sut.required_types)
