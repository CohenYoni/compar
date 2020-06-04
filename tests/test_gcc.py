import unittest
from compilers.gcc import Gcc



class TestGcc(unittest.TestCase):

    def setUp(self):
        # run before every single test
        self.version = "10.1"
        self.compilation_flags = ['flag1', 'flag2']
        self.main_c_file = "test.c"
        self.input_file_directory = "path/to/local/directory"
        self.gcc_obj = Gcc(version=self.version,
                           compilation_flags=self.compilation_flags,
                           main_c_file=self.main_c_file,
                           input_file_directory=self.input_file_directory)

    def setDown(self):
        pass
        #run after every single test


if __name__ == '__main__':
    unittest.main()
