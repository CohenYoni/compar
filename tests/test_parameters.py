from unittest import TestCase
from parameters import Parameters


class TestCodels(TestCase):

    def setUp(self):
        self.test_obj = Parameters()

    def test_json_to_obj(self):
        omp_directives_param = 'for_schedule(static, 2)'
        omp_rtl_param = 'omp_set_num_threads(32)'
        compilation_param = '-alias=3'
        dic = {'omp_directives_params': [omp_directives_param],
               'omp_rtl_params': [omp_rtl_param],
               'compilation_params': [compilation_param]
               }
        result = Parameters.json_to_obj(dic)

        self.test_obj.add_omp_directives_param(omp_directives_param)
        self.test_obj.add_omp_rtl_param(omp_rtl_param)
        self.test_obj.add_compilation_param(compilation_param)

        self.assertEqual(result.get_compilation_params(),  self.test_obj.get_compilation_params())
        self.assertEqual(result.get_omp_directives_params(),  self.test_obj.get_omp_directives_params())
        self.assertEqual(result.get_omp_rtl_params(),  self.test_obj.get_omp_rtl_params())


    def test_add_omp_directives_param(self):
        omp_directives_param_1 = 'for_schedule(static, 2)'
        omp_directives_param_2 = 'for_schedule(static, 16)'

        self.test_obj.add_omp_directives_param(omp_directives_param_1)
        result = self.test_obj.get_omp_directives_params()
        self.assertEqual(result, [omp_directives_param_1])

        self.test_obj.add_omp_directives_param(omp_directives_param_2)
        result = self.test_obj.get_omp_directives_params()
        self.assertEqual(result, [omp_directives_param_1, omp_directives_param_2])

        self.test_obj.add_omp_directives_param(omp_directives_param_1)
        result = self.test_obj.get_omp_directives_params()
        self.assertNotEqual(result, [omp_directives_param_1, omp_directives_param_2, omp_directives_param_1])

        self.test_obj.set_omp_directives_params([omp_directives_param_1])
        result = self.test_obj.get_omp_directives_params()
        self.assertEqual(result, [omp_directives_param_1])

    def test_add_omp_rtl_param(self):
        omp_rtl_param_1 = 'omp_set_num_threads(32)'
        omp_rtl_param_2 = 'omp_set_num_threads(16)'

        self.test_obj.add_omp_rtl_param(omp_rtl_param_1)
        result = self.test_obj.get_omp_rtl_params()
        self.assertEqual(result, [omp_rtl_param_1])

        self.test_obj.add_omp_rtl_param(omp_rtl_param_2)
        result = self.test_obj.get_omp_rtl_params()
        self.assertEqual(result, [omp_rtl_param_1, omp_rtl_param_2])

        self.test_obj.add_omp_rtl_param(omp_rtl_param_1)
        result = self.test_obj.get_omp_rtl_params()
        self.assertNotEqual(result, [omp_rtl_param_1, omp_rtl_param_2, omp_rtl_param_1])

        self.test_obj.set_omp_rtl_params([omp_rtl_param_1])
        result = self.test_obj.get_omp_rtl_params()
        self.assertEqual(result, [omp_rtl_param_1])

    def test_add_compilation_param(self):
        compilation_param_1 = '-alias=3'
        compilation_param_2 = '-privatize=0'

        self.test_obj.add_compilation_param(compilation_param_1)
        result = self.test_obj.get_compilation_params()
        self.assertEqual(result, [compilation_param_1])

        self.test_obj.add_compilation_param(compilation_param_2)
        result = self.test_obj.get_compilation_params()
        self.assertEqual(result, [compilation_param_1, compilation_param_2])

        self.test_obj.add_compilation_param(compilation_param_1)
        result = self.test_obj.get_compilation_params()
        self.assertNotEqual(result, [compilation_param_1, compilation_param_2, compilation_param_1])

        self.test_obj.set_compilation_params([compilation_param_1])
        result = self.test_obj.get_compilation_params()
        self.assertEqual(result, [compilation_param_1])
