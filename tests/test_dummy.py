import unittest
from compilers.dummy import Dummy
from exceptions import CompilationError


class TestClassDummy(unittest.TestCase):
    def setUp(self):
        self.dummy_mock = Dummy(version='1')

    def test_dummy_instance_is_not_none(self):
        self.assertIsNotNone(self.dummy_mock)

    def test_compile_raise_error(self):
        self.assertRaises(CompilationError, self.dummy_mock.compile)


if __name__ == '__main__':
    unittest.main()