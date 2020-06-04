import unittest
from compilers.par4all import Par4all
import os
from unittest.mock import patch
import shutil

import time

class TestPar4all(unittest.TestCase):

    def setUp(self):
        self.input_file_directory = "unit_test_par4all"


        self.version = "1.2"
        self.compilation_flags = []
        self.file_list = []
        self.include_dirs_list = []
        self.extra_files = []
        self.p4a = Par4all(version=self.version,
                           compilation_flags=self.compilation_flags,
                           input_file_directory=self.input_file_directory,
                           file_list=self.file_list,
                           include_dirs_list=self.include_dirs_list,
                           extra_files=self.extra_files)


    def setDown(self):
        pass

        #run after every single test


    def test_initiate_for_new_task(self):
        compilation_flags = ['flag1', 'flag2']
        input_file_directory = "input/file/directory"
        file_list = []
        self.p4a.initiate_for_new_task(compilation_flags=compilation_flags,
                                       input_file_directory=input_file_directory,
                                       file_list=file_list)
        self.assertEqual(self.p4a.get_compilation_flags(), compilation_flags)
        self.assertEqual(self.p4a.get_input_file_directory(), input_file_directory)

    def test_compile(self):
        c_file_code = '''#includ <stdio.h>
                          printf("helloWorld);'''
        self.input_file_directory = "unit_test_par4all"
        self.file_name = 'unit_test_par4all.p4a.c'
        self.file_path = "/unit_test_par4all/unit_test_par4all.p4a.c"
        if not os.path.exists(self.input_file_directory):
            os.mkdir(self.input_file_directory)
        with open(self.file_name, "w+") as f:
            f.write(c_file_code)

        self.p4a.set_input_file_directory(self.input_file_directory)
        self.file_list = [{"file_name": self.file_name, "file_full_path": self.file_path}]
        self.p4a.set_file_list(self.file_list)
        with patch('compilers.par4all.run_subprocess') as run_process_mock:
            run_process_mock.return_value = ('stdout', 'stderr', 'ret_code')
            self.p4a.compile()
            run_process_mock.assert_called_with(['PATH=/bin:$PATH p4a -vv '+''.join(self.file_path)+' '],
                                                self.input_file_directory)

        if os.path.exists(self.input_file_directory):
            shutil.rmtree(self.input_file_directory)

    def test_inject_code_at_the_top(self):
        c_file_code = '''#includ <stdio.h>
                         printf("helloWorld);'''
        self.input_file_directory = "unit_test_par4all"
        self.file_name = 'unit_test_par4all.c'
        self.file_path = "unit_test_par4all/unit_test_par4all.p4a.c"
        if not os.path.exists(self.input_file_directory):
            os.mkdir(self.input_file_directory)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w+") as f:
                f.write(c_file_code)

        code_to_be_injected = '//Testing par 4 all'
        Par4all.inject_code_at_the_top(self.file_path, code_to_be_injected)
        result = ''
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                result = f.readline()
        self.assertEqual(result, code_to_be_injected + '\n')
        if os.path.exists(self.input_file_directory):
            shutil.rmtree(self.input_file_directory)


    def test_remove_code_from_file(self):
        c_file_code = '''
                        //Testing par 4 all
                        #includ <stdio.h>
                        printf("helloWorld);'''

        self.input_file_directory = "unit_test_par4all"
        self.file_name = 'unit_test_par4all.c'
        self.file_path = "unit_test_par4all/unit_test_par4all.p4a.c"
        if not os.path.exists(self.input_file_directory):
            os.mkdir(self.input_file_directory)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w+") as f:
                f.write(c_file_code)

        code_to_be_removed = '//Testing par 4 all'
        Par4all.remove_code_from_file(self.file_path, code_to_be_removed)
        result = ''
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                result = f.readline()

        self.assertNotEqual(result, code_to_be_removed + '\n')
        if os.path.exists(self.input_file_directory):
            shutil.rmtree(self.input_file_directory)

if __name__ == '__main__':

    unittest.main()
