from unittest import TestCase
from database import Database
from unittest import mock
import os
from globals import ComparConfig


class TestClassDatabase(TestCase):

    @mock.patch('pymongo.MongoClient')
    def setUp(self, mock_get_db):
        self.file_path = r'tests/test_file/'
        os.makedirs(self.file_path, exist_ok=True)
        mode = ComparConfig.MODES[ComparConfig.DEFAULT_MODE]

        self.test_db = Database(self.file_path, mode)

        omp_directives_param = 'for_schedule(static, 2)'
        omp_rtl_param = 'omp_set_num_threads(32)'
        compilation_param = '-alias=3'

        self.param_dic = {'omp_directives_params': [omp_directives_param],
                     'omp_rtl_params': [omp_rtl_param],
                     'compilation_params': [compilation_param]}

        self.comb_dic = {'_id': '1',
                    'compiler_name': 'test',
                    'parameters': self.param_dic
                        }

    def tearDown(self):
        self.test_db.close_connection()

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_insert_new_combination_results(self, mock_find):
        comb = {"_id": '1', "compiler_name": "cetus", "parameters": self.param_dic}
        mock_find.return_value = {"_id": '1', "name": "tim"}

        result = self.test_db.insert_new_combination_results(comb)
        self.assertEqual(result, True)
