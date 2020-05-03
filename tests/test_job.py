import unittest
from job import Job
from combination import Combination
from parameters import Parameters


class TestCompiler(unittest.TestCase):

    def setUp(self):
        # run before every single test
        self.combination = Combination(combination_id="1234",
                                       compiler_name="test",
                                       parameters=Parameters())
        self.directory = "path/to/local/directory"
        self.exec_file_args = "x=10 y=50"
        self.job_obj = Job(directory=self.directory,
                           combination=self.combination,
                           exec_file_args=self.exec_file_args)

    def setDown(self):
        pass
        #run after every single test

    def test_set_job_id(self):
        job_id = "123"
        self.job_obj.set_job_id(job_id=job_id)
        self.assertEqual(self.job_obj.job_results["job_id"], job_id)
        self.assertEqual(self.job_obj.job_id, job_id)

    def test_get_job_id(self):
        self.assertEqual(self.job_obj.job_results["job_id"],  self.job_obj.get_job_id())

    def test_set_get_total_run_time(self):
        total_run_time = 12.54
        self.job_obj.set_total_run_time(total_run_time=total_run_time)
        self.assertEqual(self.job_obj.job_results['total_run_time'], total_run_time)
        self.assertEqual(self.job_obj.get_total_run_time(), total_run_time)

    def test_set_get_directory_path(self):
        directory_path = "new/path/to/local/directory"
        self.job_obj.set_directory_path(new_path=directory_path)
        self.assertEqual(self.job_obj.get_directory_path(), directory_path)

    def test_get_directory_name(self):
        self.assertEqual(self.job_obj.get_directory_name(), 'directory')

    def test_get_exec_file_args(self):
        self.assertEqual(self.job_obj.get_exec_file_args(), self.exec_file_args)

    def test_set_exec_file_args(self):
        exec_file_args = "z=80 r=100"
        self.job_obj.set_exec_file_args(args=exec_file_args)
        self.assertEqual(self.job_obj.get_exec_file_args(), exec_file_args)

    def test_get_combination(self):
        self.assertEqual(self.job_obj.get_combination(), self.combination)

    def test_set_combination(self):
        combination = Combination(combination_id="6798",
                                  compiler_name="test2",
                                  parameters=Parameters())
        self.job_obj.set_combination(combination=combination)
        self.assertEqual(self.job_obj.get_combination(), combination)

    def test_set_get_job_results(self):
        job_id = "1548"
        combination_id = "7894"
        run_time_results = []
        result = {
            'job_id': job_id,
            '_id': combination_id,
            'run_time_results': run_time_results}
        self.job_obj.set_job_results(job_id=job_id,
                                     combination_id=combination_id,
                                     run_time_results=run_time_results)
        self.assertEqual(self.job_obj.get_job_results(), result)

    def test_set_get_file_results(self):
        file_id_by_rel_path = "245222"
        loops = []
        result = {'file_id_by_rel_path': file_id_by_rel_path,
                  'loops': loops}
        self.job_obj.set_file_results(file_id_by_rel_path=file_id_by_rel_path)
        self.assertEqual(self.job_obj.get_file_results(file_id_by_rel_path=file_id_by_rel_path), result)

    def test_set_get_file_results_loops(self):
        file_id_by_rel_path = "245222"
        self.job_obj.set_file_results(file_id_by_rel_path=file_id_by_rel_path)
        loops = [{'loop_label': 'test_loop1',
                  'run_time': 15.4,
                  'speedup': 2.1},
                 {'loop_label': 'test_loop2',
                  'run_time': 11.4,
                  'speedup': 1.1}]

        self.job_obj.set_file_results_loops(file_id_by_rel_path=file_id_by_rel_path, loops=loops)
        self.assertEqual(self.job_obj.get_file_results_loops(file_id_by_rel_path=file_id_by_rel_path), loops)

    def test_set_get_loop_in_file_results(self):
        file_id_by_rel_path = "245222"
        self.job_obj.set_file_results(file_id_by_rel_path=file_id_by_rel_path)
        loop1_label = 'test_loop1'
        run_time = 15.4
        self.job_obj.set_loop_in_file_results(file_id_by_rel_path=file_id_by_rel_path,
                                              loop_label=loop1_label,
                                              run_time=run_time)
        loop1_result = {'loop_label': loop1_label,
                        'run_time': run_time,
                        'speedup': 0}

        self.assertEqual(self.job_obj.get_loop_in_file_results(file_id_by_rel_path=file_id_by_rel_path,
                                                               loop_label=loop1_label), loop1_result)
        loop2_label = 'test_loop2'
        loop2_result = {'loop_label': loop2_label,
                        'dead_code': True}
        self.job_obj.set_loop_in_file_results(file_id_by_rel_path=file_id_by_rel_path,
                                              loop_label=loop2_label,
                                              run_time=run_time,
                                              dead_code=True)
        self.assertEqual(self.job_obj.get_loop_in_file_results(file_id_by_rel_path=file_id_by_rel_path,
                                                               loop_label=loop2_label), loop2_result)

    def test_set_get_loop_speedup_in_file_results(self):
        file_id_by_rel_path = "245222"
        self.job_obj.set_file_results(file_id_by_rel_path=file_id_by_rel_path)
        loop_label = 'test_loop1'
        run_time = 15.4
        speedup = 3.2
        self.job_obj.set_loop_in_file_results(file_id_by_rel_path=file_id_by_rel_path,
                                              loop_label=loop_label,
                                              run_time=run_time,
                                              speedup=speedup)

        self.assertEqual(self.job_obj.get_loop_speedup_in_file_results(file_id_by_rel_path=file_id_by_rel_path,
                                                                       loop_label=loop_label), speedup)
        speedup = 8.4
        self.job_obj.set_loop_speedup_in_file_results(file_id_by_rel_path=file_id_by_rel_path,
                                                      loop_label=loop_label,
                                                      speedup=speedup)

        self.assertEqual(self.job_obj.get_loop_speedup_in_file_results(file_id_by_rel_path=file_id_by_rel_path,
                                                                       loop_label=loop_label), speedup)

    def test_set_get_loop_run_time_in_file_results(self):
        file_id_by_rel_path = "245222"
        self.job_obj.set_file_results(file_id_by_rel_path=file_id_by_rel_path)
        loop_label = 'test_loop1'
        run_time = 15.4
        speedup = 3.2
        self.job_obj.set_loop_in_file_results(file_id_by_rel_path=file_id_by_rel_path,
                                              loop_label=loop_label,
                                              run_time=run_time,
                                              speedup=speedup)

        self.assertEqual(self.job_obj.get_loop_run_time_in_file_results(file_id_by_rel_path=file_id_by_rel_path,
                                                                        loop_label=loop_label), run_time)
        run_time = 8.4
        self.job_obj.set_loop_run_time_in_file_results(file_id_by_rel_path=file_id_by_rel_path,
                                                       loop_label=loop_label,
                                                       run_time=run_time)

        self.assertEqual(self.job_obj.get_loop_run_time_in_file_results(file_id_by_rel_path=file_id_by_rel_path,
                                                                        loop_label=loop_label), run_time)


if __name__ == '__main__':
    unittest.main()

