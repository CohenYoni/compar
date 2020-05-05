import unittest
from execute_job import ExecuteJob
from job import Job
from combination import Combination
from threading import RLock
from globals import ComparMode, ComparConfig, CombinatorConfig
import os
from parameters import Parameters
from unittest.mock import patch


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
        self.db = "DB object"#need Mock
        self.db_lock = RLock()
        self.serial_run_time = {(self.file_relative_path, self.loop1_label): self.loop1_serial_run_time}  #{(<file_id_by_rel_path>, <loop_label>) : <run_time>, ... }
        self.relative_c_file_list = [{"file_name": self.file_name, "file_relative_path": self.file_relative_path }]
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
      
'''