import os
import subprocess
import unittest
from subprocess_handler import run_subprocess
from unittest.mock import patch, MagicMock


class TestSubprocessHandler(unittest.TestCase):

    def test_run_subprocess(self):
        command = " some command"
        cwd = '.'
        with patch('subprocess_handler.subprocess.Popen') as popen_mock:
            mock = MagicMock()
            mock.communicate.return_value ='std_out', 'std_err'
            mock.returncode = 0
            popen_mock.return_value = mock
            run_subprocess(command=command, cwd=cwd)
            popen_mock.assert_called_with(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, shell=True,
                                          env=os.environ, universal_newlines=True)


