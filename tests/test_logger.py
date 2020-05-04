from unittest import TestCase
from logger import *
import io
import sys

class TestCodels(TestCase):
    NO_OUTPUT = 0
    BASIC = 1
    VERBOSE = 2
    DEBUG = 3

    def setUp(self):
        initialize(1, 'tests')

    def tearDown(self):
        if os.path.exists(r'tests/compar_output.log'):
            os.remove(r'tests/compar_output.log')

    def test_get_log_level(self):
        result = get_log_level()
        self.assertEqual(result, BASIC)

    def test_info(self):
        initialize(BASIC, 'tests')
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        info('test')  # Call function.
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertEqual(capturedOutput.getvalue(), 'test\n')

    def test_verbose(self):
        initialize(VERBOSE, 'tests')
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        verbose('test')  # Call function.
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertEqual(capturedOutput.getvalue(), 'test\n')

    def test_debug(self):
        initialize(DEBUG, 'tests')
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        debug('test')  # Call function.
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertEqual(capturedOutput.getvalue(), 'test\n')

    def test_info_error(self):
        initialize(NO_OUTPUT, 'tests')
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        info_error('test')  # Call function.
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertNotEqual(capturedOutput.getvalue(), 'test\n')

    def test_verbose_error(self):
        initialize(NO_OUTPUT, 'tests')
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        verbose_error('test')  # Call function.
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertNotEqual(capturedOutput.getvalue(), 'test\n')

    def test_debug_error(self):
        initialize(DEBUG, 'tests')
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        debug_error('test')  # Call function.
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertNotEqual(capturedOutput.getvalue(), 'test\n')

    def test_log_to_file(self):
        initialize(DEBUG, 'tests')
        log_to_file('test', r'tests/compar_output.log')
        result = os.path.exists(r'tests/compar_output.log')
        self.assertEqual(result, True)

