import unittest
from compilers.compiler import Compiler


class TestCompiler(unittest.TestCase):

    def setUp(self):
        class dummy(Compiler):
            def compile(self):
               return "test_compiler"

        # run before every single test
        self.version = "10.1"
        self.compilation_flags = ['flag1', 'flag2']
        self.input_file_directory = "path/to/local/directory"
        self.compiler_obj = dummy(version=self.version,
                                  compilation_flags=self.compilation_flags,
                                  input_file_directory=self.input_file_directory)

    def setDown(self):
        pass
        #run after every single test

    def test_get_version(self):
        self.assertEqual(self.compiler_obj.get_version(), self.version)

    def test_set_version(self):
        version = "22.2"
        self.compiler_obj.set_version(version=version)
        self.assertEqual(self.compiler_obj.get_version(), version)

    def test_get_input_file_directory(self):
        self.assertEqual(self.compiler_obj.get_input_file_directory(), self.input_file_directory)

    def test_set_input_file_directory(self):
        input_file_directory = "new/path/to/local/directory"
        self.compiler_obj.set_input_file_directory(input_file_directory=input_file_directory)
        self.assertEqual(self.compiler_obj.get_input_file_directory(), input_file_directory)

    def test_get_compilation_flags(self):
        self.assertEqual(self.compiler_obj.get_compilation_flags(), self.compilation_flags)

    def test_set_compilation_flags(self):
        compilation_flags = ['flag3', 'flag5', 'flag6']
        self.compiler_obj.set_compilation_flags(compilation_flags)
        self.assertEqual(self.compiler_obj.get_compilation_flags(), compilation_flags)

    def test_initiate_for_new_task(self):
        input_file_directory = "new/path/to/local/directory"
        compilation_flags = ['flag3', 'flag5', 'flag6']
        self.compiler_obj.initiate_for_new_task(compilation_flags=compilation_flags, input_file_directory=input_file_directory )
        self.assertEqual(self.compiler_obj.get_compilation_flags(), compilation_flags)



if __name__ == '__main__':
    unittest.main()

