import unittest
import os
import shutil
import re
from compar import Compar
import exceptions as e
from globals import ComparConfig


class TestClassCompar(unittest.TestCase):
    def setUp(self):
        self.input_dir = "input_test_dir"
        self.output_dir = "output_test_dir"
        if not os.path.exists(self.input_dir):
            os.mkdir(self.input_dir)
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        self.project_name = "test_project"
        self.main_file_rel_path = os.path.join(self.input_dir, self.project_name + ".c")

        self.start_label_loop_id_1 = '// START_LOOP_MARKER_1'
        self.c_code_without_label = "void main() {\nint x = 3;\nfor(int i = 0; i < 1000; i++){\nx++;\n}\n}"
        self.c_code_with_label = self.c_code_without_label.replace('for', self.start_label_loop_id_1 + '\nfor')

    def tearDown(self):
        if os.path.exists(self.input_dir):
            shutil.rmtree(self.input_dir)
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_set_num_of_threads(self):
        num_of_threads = 24
        Compar.set_num_of_threads(num_of_threads)
        self.assertEquals(num_of_threads, Compar.NUM_OF_THREADS)
        num_of_threads = 36
        Compar.set_num_of_threads(num_of_threads)
        self.assertEquals(num_of_threads, Compar.NUM_OF_THREADS)

    def test_inject_c_code_to_loop(self):
        with self.assertRaises(e.FileError):
            Compar.inject_c_code_to_loop(self.main_file_rel_path, '1', "TEST")
        with open(self.main_file_rel_path, 'w') as file:
            file.write(self.c_code_without_label)
        Compar.inject_c_code_to_loop(self.main_file_rel_path, '1', "TEST")
        with open(self.main_file_rel_path, 'r') as file:
            self.assertEquals(self.c_code_without_label, file.read())
        with open(self.main_file_rel_path, 'w') as file:
            file.write(self.c_code_with_label)
        Compar.inject_c_code_to_loop(self.main_file_rel_path, '1', "TEST")
        with open(self.main_file_rel_path, 'r') as file:
            file_text = file.read()
        self.assertTrue("TEST" in file_text)

    def test_get_file_content(self):
        with open(self.main_file_rel_path, 'w') as file:
            file.write(self.c_code_without_label)
        self.assertEquals(self.c_code_without_label, Compar.get_file_content(self.main_file_rel_path))

    def test_add_to_loop_details_about_comp_and_combination(self):
        comp_name = 'TEST'
        combination_id = '1'
        to_replace = ''
        to_replace += f'{self.start_label_loop_id_1}\n{ComparConfig.COMBINATION_ID_C_COMMENT}{combination_id}\n'
        to_replace += f'{ComparConfig.COMPILER_NAME_C_COMMENT}{comp_name}\n'
        with open(self.main_file_rel_path, 'w') as file:
            file.write(self.c_code_with_label)
        self.assertEquals(self.c_code_with_label, Compar.get_file_content(self.main_file_rel_path))
        Compar.add_to_loop_details_about_comp_and_combination(self.main_file_rel_path, self.start_label_loop_id_1,
                                                              combination_id, comp_name)
        with open(self.main_file_rel_path, 'r') as file:
            file_text = file.read()
        self.assertEquals(file_text, re.sub(f'{self.start_label_loop_id_1}[ ]*\\n', to_replace, self.c_code_with_label))

    def test_remove_optimal_combinations_details(self):
        comp_name = 'TEST'
        combination_id = '1'
        with open(self.main_file_rel_path, 'w') as file:
            file.write(self.c_code_with_label)
        Compar.add_to_loop_details_about_comp_and_combination(self.main_file_rel_path, self.start_label_loop_id_1,
                                                              combination_id, comp_name)
        with open(self.main_file_rel_path, 'r') as file:
            file_text = file.read()
        self.assertTrue("COMBINATION_ID" in file_text)
        Compar.remove_optimal_combinations_details([self.main_file_rel_path])
        with open(self.main_file_rel_path, 'r') as file:
            file_text = file.read()
        self.assertFalse("COMBINATION_ID" in file_text)


if __name__ == '__main__':
    unittest.main()
