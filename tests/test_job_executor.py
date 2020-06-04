import unittest
from job_executor import JobExecutor
from unittest.mock import patch


class TestJobExecutor(unittest.TestCase):

    def setUp(self):
        self.number_of_threads = 5
        self.job_exe_obj = JobExecutor(self.number_of_threads)

    def setDown(self):
        pass

    def test_create_jobs_pool(self):
        with patch('job_executor.ThreadPoolExecutor') as Thread_Pool_mock:
            Thread_Pool_mock.return_value = True
            self.job_exe_obj.create_jobs_pool()
            Thread_Pool_mock.assert_called_with(max_workers=self.number_of_threads, thread_name_prefix="compar_job_thread")

    def test_run_job_in_thread(self):
        self.job_exe_obj.create_jobs_pool()

        def foo():
            print("Testing")
        job = "job"
        self.job_exe_obj.run_job_in_thread(foo, job)

    def test_wait_and_finish_pool(self):
        self.job_exe_obj.create_jobs_pool()
        self.job_exe_obj.wait_and_finish_pool()




