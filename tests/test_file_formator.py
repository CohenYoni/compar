import unittest
import os
import file_formator as f
from globals import FileFormatorConfig


class TestFileFormator(unittest.TestCase):
    def setUp(self):
        self.file_name = "test_file.c"
        self.c_code = "void main() {\nint x = 3;\nfor(int i = 0; i < 1000; i++){\nx++;\n}\n}"

        self.test_file = open(self.file_name, 'w')
        self.test_file.write(self.c_code)
        self.test_file.close()

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_comment_directives(self):
        text = self.c_code
        new_text = f.comment_directives(text)
        self.assertEqual(self.c_code, new_text)

        text = '#pragma' + '\n' + text
        new_text = f.comment_directives(text)
        self.assertEqual(new_text, FileFormatorConfig.COMMENT_PREFIX + text)

    def test_uncomment_directives(self):
        text = self.c_code
        new_text = f.uncomment_directives(text)
        self.assertEqual(text, new_text)

        text = FileFormatorConfig.COMMENT_PREFIX + '#pragma\n' + text
        new_text = f.uncomment_directives(text)
        self.assertNotEqual(text, new_text)
        text = text.replace(FileFormatorConfig.COMMENT_PREFIX, '')
        self.assertEqual(new_text, text)

    def test_get_format_command(self):
        style_arguments = ', '.join(FileFormatorConfig.STYLE_ARGUMENTS)
        style_arguments = f'\"{{{style_arguments}}}\"'
        format_command = ['source', 'scl_source', 'enable', 'llvm-toolset-7', '&&']
        format_command += ['clang-format', '-i'] + [self.file_name] + ['-style', style_arguments]
        res = f.get_format_command([self.file_name], False)
        self.assertIsNotNone(res)
        self.assertEqual(res, format_command)


if __name__ == '__main__':
    unittest.main()