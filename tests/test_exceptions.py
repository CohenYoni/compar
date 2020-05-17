import unittest
import os
import shutil
import exceptions as e
from globals import CombinationValidatorConfig


class TestExceptions(unittest.TestCase):
    def setUp(self):
        self.path = 'test/test'

        self.file_name = "test_file.txt"
        self.file_text = "IT'S A TEST!"
        self.file = open(self.file_name, 'w')
        self.file.write(self.file_text)
        self.file.close()

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        if os.path.exists(self.path):
            shutil.rmtree(self.path)

    def test_assert_file_exist(self):
        self.assertIsNone(e.assert_file_exist(self.file_name))
        with self.assertRaises(e.FileError):
            e.assert_file_exist('Does Not Exists')
            
    def test_assert_file_from_format(self):
        self.assertIsNone(e.assert_file_from_format(self.file_name, 'txt'))
        with self.assertRaises(e.FileError):
            e.assert_file_from_format(self.file_name, 'c')

    def test_assert_file_is_empty(self):
        self.assertIsNone(e.assert_file_is_empty(self.file_name))
        with self.assertRaises(e.FileError):
            e.assert_file_is_empty('')

    def test_assert_forbidden_characters(self):
        self.assertIsNone(e.assert_forbidden_characters(self.path))
        with self.assertRaises(e.UserInputError):
            e.assert_forbidden_characters(self.path + '}')
        with self.assertRaises(e.UserInputError):
            e.assert_forbidden_characters('{' + self.path)

    def test_assert_test_file_name(self):
        self.assertIsNone(e.assert_test_file_name(CombinationValidatorConfig.UNIT_TEST_FILE_NAME))
        with self.assertRaises(e.UserInputError):
            e.assert_test_file_name(self.file_name)

    def test_assert_test_file_function_name(self):
        with self.assertRaises(e.UserInputError):
            e.assert_test_file_function_name(self.path)

    def test_assert_folder_exist(self):
        # self.assertIsNone(e.assert_folder_exist(self.path))
        with self.assertRaises(e.FolderError):
            e.assert_folder_exist(self.path)


if __name__ == '__main__':
    unittest.main()

