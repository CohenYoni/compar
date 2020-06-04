from collections import Generator
from unittest import TestCase
from unittest.mock import MagicMock
import database
import exceptions
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

    def test_get_project_name(self):
        result = self.test_db.get_project_name()
        self.assertEqual(result, self.file_path)

    def test_get_new_collection_name(self):
        original_collection_name = 'test_collection_name'
        result = self.test_db.get_new_collection_name(original_collection_name)
        self.assertEqual(result, f"{original_collection_name}_{1}")

    @mock.patch.object(database.Database, 'create_static_db')
    def test_create_collections(self, db_mock):
        self.test_db.create_collections()
        db_mock.assert_called_once()

    def test_is_collection_exists(self):
        result = self.test_db.is_collection_exists('no_exist')
        self.assertEqual(result, False)

    def test_initialize_static_db(self):
        result = self.test_db.initialize_static_db()
        self.assertEqual(result, 97)

    def test_combination_has_results(self):
        result = self.test_db.combination_has_results(self.test_db.SERIAL_COMBINATION_ID)
        self.assertEqual(result, True)

    def test_combinations_iterator(self):
        result = self.test_db.combinations_iterator()
        self.assertEqual(isinstance(result, Generator), True)

    def test_delete_combination(self):
        result = self.test_db.delete_combination(self.test_db.SERIAL_COMBINATION_ID)
        self.assertEqual(result, True)

    def test_find_optimal_loop_combination(self):
        self.assertRaises(exceptions.DeadCodeFile, self.test_db.find_optimal_loop_combination, '1', '99')

    def test_get_combination_results(self):
        result = self.test_db.get_combination_results(self.test_db.SERIAL_COMBINATION_ID)
        self.assertEqual(isinstance(result, MagicMock), True)

    def test_get_combination_from_static_db(self):
        expected = {'_id': 'serial', 'compiler_name': 'serial', 'parameters': {'omp_rtl_params': [],
                                                                               'omp_directives_params': [],
                                                                               'compilation_params': []}}
        result = self.test_db.get_combination_from_static_db(self.test_db.SERIAL_COMBINATION_ID)
        self.assertEqual(result, expected)

    def test_get_total_runtime_best_combination(self):
        result = self.test_db.get_total_runtime_best_combination()
        self.assertEqual(isinstance(result, MagicMock), True)

    def test_remove_unused_data(self):
        result = self.test_db.remove_unused_data(self.test_db.SERIAL_COMBINATION_ID)
        self.assertEqual(result, None)

    def test_get_final_result_speedup_and_runtime(self):
        expected = (1.0, 1.0)
        result = self.test_db.get_final_result_speedup_and_runtime()
        self.assertEqual(result, expected)
