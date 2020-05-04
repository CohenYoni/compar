from unittest import TestCase
from combinator import *


class TestCodels(TestCase):

    def setUp(self):
        self.test_directive_params = ['for_schedule(static, 2)', 'for_schedule(static, 4)', 'for_schedule(static, 8)',
                                      'for_schedule(static, 16)', 'for_schedule(static, 32)', 'for_schedule(dynamic)']
        self.test_compilation_params = [['-parallelize-loops=1', '-parallelize-loops=2'],
                                        ['-reduction=0', '-reduction=2'], ['-privatize=0', '-privatize=2'],
                                        ['-alias=1', '-alias=3']]
        self.test_rtl_params = [['omp_set_num_threads(2);', 'omp_set_num_threads(4);', 'omp_set_num_threads(8);',
                                 'omp_set_num_threads(16);', 'omp_set_num_threads(32);']]

    def tearDown(self):
        pass

    def test_generate_omp_directive_params(self):
        result = generate_omp_directive_params()
        self.assertEqual(result,  self.test_directive_params)

    def test_generate_directive_list_from_json(self):
        with open(OMP_DIRECTIVES_FILE_PATH, 'r') as fp:
            json_omp_directives = json.load(fp)
        params = json_omp_directives['for']
        pragma_type = FOR_DIRECTIVE_PREFIX
        result = generate_directive_list_from_json(params, pragma_type)
        self.assertEqual(result,  [self.test_directive_params])

    def test_generate_toggle_params_list(self):
        with open(COMPILATION_PARAMS_FILE_PATH, 'r') as fp:
            compilation_flags_array = json.load(fp)
        comb = compilation_flags_array[0]
        compiler = comb["compiler"]
        result = generate_toggle_params_list(comb["essential_params"]["toggle"], True)
        self.assertEqual(result,  [])

    def test_generate_valued_params(self):
        with open(COMPILATION_PARAMS_FILE_PATH, 'r') as fp:
            compilation_flags_array = json.load(fp)
        comb = compilation_flags_array[0]
        compiler = comb["compiler"]
        result = generate_valued_params_list(comb["optional_params"]["valued"], True)
        self.assertEqual(result, self.test_compilation_params)

    def test_generate_omp_rtl_params(self):
        result = []
        with open(OMP_RTL_PARAMS_FILE_PATH, 'r') as fp:
            omp_rtl_array = json.load(fp)
        for param in omp_rtl_array:
            result.append(generate_omp_rtl_params(param))
        self.assertEqual(result,  self.test_rtl_params)

    def test_mult_lists(self):
        test = ['omp_set_num_threads(2);', 'omp_set_num_threads(4);', 'omp_set_num_threads(8);',
                'omp_set_num_threads(16);', 'omp_set_num_threads(32);']

        omp_rtl_params = []
        with open(OMP_RTL_PARAMS_FILE_PATH, 'r') as fp:
            omp_rtl_array = json.load(fp)
        for param in omp_rtl_array:
            omp_rtl_params.append(generate_omp_rtl_params(param))

        result = mult_lists(omp_rtl_params)
        self.assertEqual(result,  test)
