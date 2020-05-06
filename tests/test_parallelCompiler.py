import os
import shutil
from unittest import TestCase
from combination import Combination
from compilers.parallelCompiler import ParallelCompiler


class TestClassParallelCompiler(TestCase):

    def setUp(self):
        self.test_comb_obj = Combination('1', 'test', None)

        os.makedirs(r'tests/test_files', exist_ok=True)
        self.test_file = open(r'tests/test_files/test_file.c', "w")
        self.test_file.write('a')
        self.test_file.close()

        self.version = "1.2"
        file_list = []
        dirs_list = []
        self.test_obj = ParallelCompiler(version=self.version, input_file_directory=r'tests/test_files',
                                         file_list=file_list, include_dirs_list=dirs_list)

    def tearDown(self):
        shutil.rmtree(r'tests/test_files')

    def test_initiate_for_new_task(self):
        compilation_flags = ['flag1', 'flag2']
        input_file_directory = "input/file/directory"
        file_list = []
        self.test_obj.initiate_for_new_task(compilation_flags=compilation_flags,
                                         input_file_directory=input_file_directory,
                                         file_list=file_list)
        self.assertEqual(self.test_obj.get_compilation_flags(), compilation_flags)
        self.assertEqual(self.test_obj.get_input_file_directory(), input_file_directory)

    def test_set_file_list(self):
        self.test_obj.set_file_list(['test1.c', 'test2.c'])
        self.assertEqual(self.test_obj.get_file_list(),  ['test1.c', 'test2.c'])