from unittest import TestCase
from combination import Combination


class TestCodels(TestCase):

    def setUp(self):
        self.test_obj = Combination('1', 'test', None)

    def test_json_to_obj(self):

        omp_directives_param = 'for_schedule(static, 2)'
        omp_rtl_param = 'omp_set_num_threads(32)'
        compilation_param = '-alias=3'

        param_dic = {'omp_directives_params': [omp_directives_param],
                     'omp_rtl_params': [omp_rtl_param],
                     'compilation_params': [compilation_param]}

        comb_dic = {'_id': '1',
                    'compiler_name': 'test',
                    'parameters': param_dic
                    }

        result = Combination.json_to_obj(comb_dic)

        self.assertEqual(result.get_combination_id(),  self.test_obj.get_combination_id())
        self.assertEqual(result.get_compiler(),  self.test_obj.get_compiler())
        self.assertEqual(self.test_obj.get_parameters(), None)
