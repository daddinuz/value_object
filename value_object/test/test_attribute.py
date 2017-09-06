import unittest
from value_object import Attribute


class TestAttribute(unittest.TestCase):
    def test_attribute_without_specifying_types(self):
        with self.assertRaises(AssertionError):
            Attribute()
        with self.assertRaises(AssertionError):
            Attribute(nullable=True)

    def test_attribute_with_none_type(self):
        with self.assertRaises(AssertionError):
            Attribute(None)

    def test_attribute_with_one_non_nullable_type(self):
        EXPECTED_TYPES = (str,)
        NOT_EXPECTED_TYPES = (int, float, list, dict, type(None))

        sut = Attribute(*EXPECTED_TYPES)

        for t in EXPECTED_TYPES:
            self.assertTrue(sut.is_valid(t()))
        for t in NOT_EXPECTED_TYPES:
            self.assertFalse(sut.is_valid(t()))

    def test_attribute_with_many_non_nullable_types(self):
        EXPECTED_TYPES = (str, int, list)
        NOT_EXPECTED_TYPES = (float, dict, type(None))

        sut = Attribute(*EXPECTED_TYPES)

        for t in EXPECTED_TYPES:
            self.assertTrue(sut.is_valid(t()))
        for t in NOT_EXPECTED_TYPES:
            self.assertFalse(sut.is_valid(t()))

    def test_attribute_with_one_nullable_type(self):
        EXPECTED_TYPES = (str,)
        NOT_EXPECTED_TYPES = (int, float, list, dict,)

        sut = Attribute(*EXPECTED_TYPES, nullable=True)

        for t in EXPECTED_TYPES:
            self.assertTrue(sut.is_valid(t()))
        self.assertTrue(sut.is_valid(None))

        for t in NOT_EXPECTED_TYPES:
            self.assertFalse(sut.is_valid(t()))

    def test_attribute_with_many_nullable_types(self):
        EXPECTED_TYPES = (str, int, float)
        NOT_EXPECTED_TYPES = (list, dict,)

        sut = Attribute(*EXPECTED_TYPES, nullable=True)

        for t in EXPECTED_TYPES:
            self.assertTrue(sut.is_valid(t()))
        self.assertTrue(sut.is_valid(None))

        for t in NOT_EXPECTED_TYPES:
            self.assertFalse(sut.is_valid(t()))
