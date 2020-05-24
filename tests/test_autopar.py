import unittest
from compilers.autopar import Autopar
import exceptions as e


class TestClassAutopar(unittest.TestCase):
    def setUp(self):
        self.autopar_mock = Autopar(version='1')
        self.input_file_directory = "test_autopar"

    def test_autopar_instance_is_not_none(self):
        self.assertIsNotNone(self.autopar_mock)

    def test_raises_exception(self):
        with self.assertRaises(e.CompilationError):
            self.autopar_mock.compile()


if __name__ == '__main__':
    unittest.main()