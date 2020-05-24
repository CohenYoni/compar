import unittest
from compilers.binaryCompiler import BinaryCompiler
import exceptions as e
from globals import GlobalsConfig
import os
import shutil


class TestClassDummy(unittest.TestCase):
    def setUp(self):
        self.binary_compiler_mock = BinaryCompiler(compiler_name='gcc', version='1')

        self.c_file_code = GlobalsConfig.OMP_HEADER + '\n#include <stdio.h>\nint main()' \
                                                      '{\nprintf("Hello, World!");\nreturn 0;\n}\n'
        self.c_main_file_name = 'test.c'
        self.directory_name = 'test_dir'
        self.file_path = self.directory_name + '/' + self.c_main_file_name
        if not os.path.exists(self.directory_name):
            os.mkdir(self.directory_name)
        with open(self.file_path, "w") as f:
            f.write(self.c_file_code)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        if os.path.exists(self.directory_name):
            shutil.rmtree(self.directory_name)

    def test_binary_compiler_instance_is_not_none(self):
        self.assertIsNotNone(self.binary_compiler_mock)

    def test_raises_exception(self):
        with self.assertRaises(e.CompilationError):
            self.binary_compiler_mock.compile()

        self.binary_compiler_mock.set_main_c_file(self.c_main_file_name)
        self.binary_compiler_mock.set_input_file_directory(self.directory_name)
        with self.assertRaises(e.CombinationFailure):
            self.binary_compiler_mock.compile()
