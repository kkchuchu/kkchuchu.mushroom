import sys
import json
import unittest
import os
import datetime
from unittest.mock import patch
from joblib import dump, load
import numpy as np
import shutil
import pytz

from ktool.util import TS, IP
from ktool.input import DataManager, RemoteSFTPConnector

import paramiko


class TestInput(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        cls.seed = 10

    @classmethod
    def teardown_class(cls):
        """Run only once in the testcases
        """
        try:
            # folder_path = cls.config._get_log_base_folder()
            # shutil.rmtree(folder_path, ignore_errors=True)
            pass
        except FileNotFoundError as e:
            pass

    def tearDown(self):
        self.input_.recycle()
        pass

    def setUp(self):
        self.input_ = DataManager(project_name="test", root_folder="./")

    def test_remote_sftp_connector__auth_fail(self):
        try:
            con = RemoteSFTPConnector('localhost')
        except paramiko.ssh_exception.SSHException as e:
            pass
        pass
