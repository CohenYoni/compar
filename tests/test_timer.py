import unittest
import os
from timer import Timer


class TestClassTimer(unittest.TestCase):
    def setUp(self):
        self.test_file = open("test_file.c", "w")
        self.c_code = "void main() {\nint x = 3;\nfor(int i = 0; i < 1000; i++){\nx++;\n}\n}"

        self.test_file.write(self.c_code)
        self.test_file.close()

        self.timer_mock = Timer("test_file.c")

    def test_get_file_name_prefix_token(self):
        prefix_output_file = '#)$-@,(&=!+%^____,(&=__compar__@__should_+__be_+%___unique_(&!+$-=!+@%=!'
        self.assertEqual(Timer.get_file_name_prefix_token(), prefix_output_file)
        if os.path.exists("test_file.c"):
            os.remove("test_file.c")


if __name__ == '__main__':
    unittest.main()


