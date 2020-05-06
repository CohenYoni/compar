import os
import shutil
from unittest import TestCase

from mongomock import patch

from compilers.cetus import Cetus
import unittest
from compilers.par4all import Par4all
import os
from unittest.mock import patch
import shutil

import time

from globals import GlobalsConfig


class TestClassCetus(TestCase):

    def setUp(self):
        os.makedirs(r'tests/test_files', exist_ok=True)
        self.test_file = open(r'tests/test_files/test_file.c', "w")
        self.test_file.write('a')

        self.test_file.close()

        self.input_file_directory = "test_cetus"

        self.version = "1.2"
        self.compilation_flags = ['-alias=3']
        self.file_list = []
        self.include_dirs_list = []
        self.extra_files = []
        self.cetus = Cetus(version=self.version,
                           compilation_flags=self.compilation_flags,
                           input_file_directory=self.input_file_directory,
                           file_list=self.file_list,
                           include_dirs_list=self.include_dirs_list,
                           extra_files=self.extra_files)

    def tearDown(self):
        if os.path.exists(self.input_file_directory):
            shutil.rmtree(self.input_file_directory)
        if os.path.exists(r'tests/test_files'):
            shutil.rmtree(r'tests/test_files')

    def test_compile(self):

        c_file_code = GlobalsConfig.OMP_HEADER + \
                      '\n#include <stdio.h>\nint main(){\nprintf("Hello, World!");\nreturn 0;\n}\n'

        self.file_name = 'test_cetus.c'
        self.file_path = "test_cetus/test.c"
        if not os.path.exists(self.input_file_directory):
            os.mkdir(self.input_file_directory)
        with open(self.file_path, "w+") as f:
            f.write(c_file_code)

        self.cetus.set_input_file_directory(self.input_file_directory)
        self.file_list = [{"file_name": self.file_name, "file_full_path": self.file_path}]
        self.cetus.set_file_list(self.file_list)
        with patch('compilers.cetus.run_subprocess') as run_process_mock:
            run_process_mock.return_value = ('stdout', 'stderr', 'ret_code')
            self.cetus.compile()
            run_process_mock.assert_called_with(['cetus -alias=3 '+''.join(self.file_name)],
                                                self.input_file_directory)

    def test_initiate_for_new_task(self):
        compilation_flags = ['flag1', 'flag2']
        input_file_directory = "input/file/directory"
        file_list = []
        self.cetus.initiate_for_new_task(compilation_flags=compilation_flags,
                                         input_file_directory=input_file_directory,
                                         file_list=file_list)
        self.assertEqual(self.cetus.get_compilation_flags(), compilation_flags)
        self.assertEqual(self.cetus.get_input_file_directory(), input_file_directory)

    def test_replace_line_in_code(self):
        Cetus.replace_line_in_code(r'tests/test_files/test_file.c', 'a', 'b')
        with open(r'tests/test_files/test_file.c', errors='ignore', mode='r') as f:
            result = f.read()
            self.assertNotEqual(result, 'a')
            self.assertEqual(result, 'b')

    def test_inject_line_in_code(self):
        Cetus.inject_line_in_code(r'tests/test_files/test_file.c', 'a')
        with open(r'tests/test_files/test_file.c', errors='ignore', mode='r') as f:
            result = f.read()
            self.assertNotEqual(result, 'ba')
            self.assertEqual(result, 'aa')