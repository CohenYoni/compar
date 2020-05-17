import unittest
import os
from timer import Timer


class TestClassTimer(unittest.TestCase):
    def setUp(self):
        self.file_name = "test_file.c"
        self.c_code = "void main() {\nint x = 3;\nfor(int i = 0; i < 1000; i++){\nx++;\n}\n}"
        self.test_loop_dict = {self.file_name: [1, 'loop_array']}

        self.test_file = open(self.file_name, 'w')
        self.test_file.write(self.c_code)
        self.test_file.close()

        self.timer_mock = Timer(self.file_name)

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_get_file_name_prefix_token(self):
        prefix_output_file = '#)$-@,(&=!+%^____,(&=__compar__@__should_+__be_+%___unique_(&!+$-=!+@%=!'
        self.assertEqual(Timer.get_file_name_prefix_token(), prefix_output_file)

    def test_inject_declarations_to_main_file(self):
        declarations_for_test = "This is a test!!"
        Timer.inject_declarations_to_main_file(self.file_name, declarations_for_test)
        with open(self.file_name, 'r') as input_file:
            file_text = input_file.read()
        self.assertTrue(declarations_for_test in file_text)
        self.assertTrue(Timer.DECL_GLOBAL_STRUCT_CODE in file_text)
        self.assertTrue(Timer.DECL_GLOBAL_TIMER_VAR_CODE in file_text)

    def test_inject_global_declaration(self):
        name_of_global_array_for_test = 'TEST_GLOBAL_ARRAY'
        with open(self.file_name, 'r') as input_file:
            file_text = input_file.read()
        new_code = Timer.inject_global_declaration(file_text, 1, name_of_global_array_for_test)
        expected_code = Timer.DECL_GLOBAL_STRUCT_CODE
        expected_code += f"{Timer.COMPAR_VAR_PREFIX}struct extern {name_of_global_array_for_test}[1];\n"
        expected_code += file_text
        self.assertEqual(new_code, expected_code)

    def test_generate_at_exit_function_code(self):
        expected_sub_code = f'if ({self.test_loop_dict[self.file_name][1]}[0].counter > 0) '
        expected_sub_code += Timer.WRITE_TO_FILE_CODE_2.format(self.test_loop_dict[self.file_name][1], 0+1,
                                                               f'{self.test_loop_dict[self.file_name][1]}'
                                                               f'[0].total_runtime')
        code = Timer.generate_at_exit_function_code(self.test_loop_dict, '')
        self.assertIsNotNone(code)
        self.assertTrue(expected_sub_code in code)

    def test_inject_atexit_code_to_main_file(self):
        code = Timer.inject_atexit_code_to_main_file(self.file_name, self.test_loop_dict, '')
        self.assertIsNone(code)


if __name__ == '__main__':
    unittest.main()


