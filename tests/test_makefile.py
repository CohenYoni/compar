import os
import shutil
import subprocess
from unittest import TestCase
from compilers.makefile import Makefile


class TestClassMakefile(TestCase):

    def setUp(self):
        self.file_path = r'tests/test_file/'
        self.file_name = 'test_file'

        os.makedirs(self.file_path, exist_ok=True)
        self.test_file = open(self.file_path+self.file_name+'.c', "w")
        self.test_file.write('#include <stdio.h>\nint main(){\nprintf("Hello, World!");\nreturn 0;\n}\n')
        self.test_file.close()
        subprocess.run(['gcc {} -o {}'.format(self.file_name+'.c', self.file_name+'.o')], shell=True, cwd=self.file_path)

        self.test_obj = Makefile(working_directory=self.file_path,
                                 exe_folder_relative_path='',
                                 exe_file_name=self.file_name+'.o',
                                 commands=['gcc '+self.file_name+'.c'])

    def tearDown(self):
        shutil.rmtree(self.file_path)

    def test_run_makefile(self):
        self.test_obj.run_makefile()
        result = os.path.exists(self.file_path+'a.out')
        self.assertEqual(result, True)

    def test_get_exe_full_path(self):
        result = self.test_obj.get_exe_full_path()
        self.assertEqual(result, self.file_path+self.file_name+'.x')

    def test_move_exe_to_base_dir(self):
        result = self.test_obj.move_exe_to_base_dir()
        self.assertEqual(result, self.file_path+self.file_name+'.x')

