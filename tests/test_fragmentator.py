import unittest
import os
from fragmentator import Fragmentator
import exceptions as e


class TestClassFragmentator(unittest.TestCase):
    def setUp(self):
        self.file_name = "test_file.c"
        self.c_code = "void main() {\nint x = 3;\nfor(int i = 0; i < 1000; i++){\nx++;\n}\n}"

        self.test_file = open(self.file_name, 'w')
        self.test_file.write(self.c_code)
        self.test_file.close()

        self.fragmentator_mock = Fragmentator(self.file_name, False)

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_fragmentator_instance_is_not_none(self):
        self.assertIsNotNone(self.fragmentator_mock)

    def test_get_file_path(self):
        self.assertEqual(self.fragmentator_mock.get_file_path(), self.file_name)

    def test_set_file_path(self):
        not_exist_path = 'path_does_not_exist.c'
        exist_path = 'path_exist.c'
        with self.assertRaises(e.FileError):
            self.fragmentator_mock.set_file_path(not_exist_path)

        file = open(exist_path, 'w')
        file.write('TEST!')
        file.close()

        self.fragmentator_mock.set_file_path(exist_path)
        self.assertEqual(self.fragmentator_mock.get_file_path(), exist_path)

        self.fragmentator_mock.set_file_path(self.file_name)

        if os.path.exists(exist_path):
            os.remove(exist_path)

    def test_count_loops_in_prepared_file_without_markers(self):
        num_of_loops = Fragmentator.count_loops_in_prepared_file(self.file_name)
        self.assertEqual(num_of_loops, 0)


if __name__ == '__main__':
    unittest.main()
