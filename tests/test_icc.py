import unittest
from unittest.mock import patch
from compilers.icc import Icc
import os
import shutil


class TestIcc(unittest.TestCase):

    def setUp(self):
        # run before every single test
        self.input_file_directory = "unit_test_icc"
        self.file_name = 'unit_test_icc.c'
        self.file_path = os.path.join(self.input_file_directory, self.file_name)
        self.version = "10.1"
        self.compilation_flags = ['flag1', 'flag2']
        self.main_c_file = "test.c"
        self.icc_obj = Icc(version=self.version,
                           compilation_flags=self.compilation_flags,
                           main_c_file=self.main_c_file,
                           input_file_directory=self.input_file_directory)

    def setDown(self):
        pass
        #run after every single test



    def test_run_compiler(self):
        c_file_code = '''#includ <stdio.h>
                         printf("helloWorld);'''
        if not os.path.exists(self.input_file_directory):
            os.mkdir(self.input_file_directory)
        with open(self.file_name, "w+") as f:
            f.write(c_file_code)

        with patch('compilers.icc.run_subprocess') as run_process_mock:
            run_process_mock.return_value = ('stdout', 'stderr', 'ret_code')
            self.icc_obj.run_compiler()
            run_process_mock.assert_called_with([self.icc_obj.get_compiler_name()] + ["-fopenmp"]
                                                + self.compilation_flags + [self.main_c_file]
                                                + ["-o"] + [self.input_file_directory + ".x"],
                                                self.input_file_directory)

        if os.path.exists(self.input_file_directory):
            shutil.rmtree(self.input_file_directory)


if __name__ == '__main__':
    unittest.main()
