import unittest
from execute_job import ExecuteJob
from job import Job
from combination import Combination
from threading import RLock
from globals import ComparConfig
import os
from parameters import Parameters
from unittest.mock import patch
from unittest.mock import Mock
import shutil


class TestExecuteJob(unittest.TestCase):

    def setUp(self):
        self.input_file_directory = "unit_test_execute_job"
        self.file_name = "unit_test_execute_job.c"

        self.file_output = "unit_test_execute_job.output.c"
        self.file_relative_path = os.path.join(self.input_file_directory, self.file_name)
        self.combination_id = "123"
        self.compiler_name = "cetus"

        self.job = Job(directory=self.input_file_directory,
                       combination=Combination(combination_id=self.combination_id,
                                               compiler_name=self.compiler_name,
                                               parameters=Parameters()))


        self.loop1_label = "3333"
        self.loop1_serial_run_time = "12.2"

        self.num_of_loops_in_files = {}
        self.db = Mock()
        self.db_lock = RLock()

        self.serial_run_time = {(self.file_relative_path, self.loop1_label): self.loop1_serial_run_time}  #{(<file_id_by_rel_path>, <loop_label>) : <run_time>, ... }
        self.relative_c_file_list = [{"file_name": self.file_name, "file_relative_path": self.file_relative_path}]
        self.slurm_partition = ComparConfig.DEFAULT_SLURM_PARTITION
        self.test_file_path = os.path.join(self.input_file_directory, self.file_output)

        self.ej = ExecuteJob(job=self.job,
                             num_of_loops_in_files=self.num_of_loops_in_files,
                             db=self.db,
                             db_lock=self.db_lock,
                             serial_run_time=self.serial_run_time,
                             relative_c_file_list=self.relative_c_file_list,
                             slurm_partition=self.slurm_partition,
                             test_file_path=self.test_file_path,
                             )
        self.ej.job.set_file_results(self.file_relative_path)
        loops = [{'loop_label': self.loop1_label,
                  'run_time': "15.5",
                  'speedup': 0},
                 {'loop_label': "124",
                  'dead_code': True}]

        self.ej.job.set_file_results_loops(self.file_relative_path, loops)

    def setDown(self):
        pass
        #run after every single test

    def test_update_speedup(self):
        self.ej.update_speedup()
        self.assertEqual(float(self.loop1_serial_run_time) / float(self.ej.job.get_loop_run_time_in_file_results(self.file_relative_path, self.loop1_label)),
                         float(self.ej.job.get_loop_speedup_in_file_results(self.file_relative_path, self.loop1_label)))

    def test_update_dead_code_files(self):
        dead_file_name = "unit_test_execute_job_dead_file.c" # not in self.relative_c_file_list
        self.relative_c_file_list.append({"file_name": dead_file_name,
                                          "file_relative_path":  os.path.join(self.input_file_directory,
                                                                              dead_file_name)})
        self.ej.update_dead_code_files()
        job_results = self.ej.job.get_job_results()['run_time_results']
        self.assertTrue(job_results[1]['dead_code_file'])


    def test_save_successful_job(self):
        self.db.insert_new_combination_results('{"key": "value"}')
        self.db.insert_new_combination_results.return_value = True
        self.ej.save_successful_job()
        self.db.insert_new_combination_results.assert_called_with(self.ej.job.get_job_results())

    def test_save_combination_as_failure(self):
        self.db.insert_new_combination_results('{"key": "value"}')
        self.db.insert_new_combination_results.return_value = True
        self.ej.save_combination_as_failure("error_msg")
        self.db.insert_new_combination_results.assert_called_with({'_id': self.combination_id, 'error': 'error_msg'})


    def test_run(self):
        user_slurm_parameters = []
        batch_dir_file_path = "unit_test_execute_job"
        if not os.path.exists(batch_dir_file_path):
            os.mkdir(batch_dir_file_path)

        with patch('execute_job.run_subprocess') as run_process_mock:
            run_process_mock.side_effect = [('stdout', 'stderr', 'ret_code')]
            with patch('execute_job.time.sleep') as sleep_mock:
                sleep_mock.return_value = True
                self.ej.run(user_slurm_parameters)
            run_process_mock.assert_any_call("sbatch  -o unit_test_execute_job/unit_test_execute_job.log unit_test_execute_job/batch_job.sh unit_test_execute_job/unit_test_execute_job.x")
            run_process_mock.assert_any_call("squeue -j  --format %t")
        if os.path.exists(self.input_file_directory):
            shutil.rmtree(self.input_file_directory)





if __name__ == '__main__':
    unittest.main()

'''
 self.job.job_results => {'job_id': "123",
                          '_id': "212"<its a combination id>
                          'run_time_results': [ { 'file_id_by_rel_path': "/test1/1234.C",
                                                'loops': [{'loop_label': "#123"
                                                            'run_time': "15.5"
                                                            'speedup': 0 <float?>
                                                           },
                                                           {'loop_label': "#124"
                                                            'dead_code': True <boolean>
                                                           },
                                                           {'loop_label': "#153"
                                                            'run_time': "18.32"
                                                            'speedup': 0 <float?>
                                                            }
                                                           ]
                                                },
                                                { 'file_id_by_rel_path': "/test1/564.C",
                                                  'loops': [ {'loop_label': "#523"
                                                              'dead_code': False <boolean>
                                                              'run_time': "1.5"
                                                              'speedup': 0 <float?>
                                                              },
                                                              { 'loop_label': "#124"
                                                                'dead_code': True <boolean>
                                                              }
                                                            ]
                                                }
                                              ]


combinations :
{'_id' : 1234 , 'compiler_name': cetus , 'parameters': '' }      
'''