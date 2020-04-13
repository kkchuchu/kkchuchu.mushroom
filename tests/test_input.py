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

import paramiko
import pandas as pd

from ktool.util import TS, IP
from ktool.input import DataManager, RemoteSFTPConnector


class TestInput(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        cls.seed = 10
        cls.root_folder = "./test_noob"

    @classmethod
    def teardown_class(cls):
        """Run only once in the testcases
        """
        try:
            shutil.rmtree(cls.root_folder, ignore_errors=True)
        except FileNotFoundError as e:
            pass

    def setUp(self):
        self.input_ = DataManager(
            project_name=self.root_folder, root_folder="./", metadata_folder= self.root_folder + "/meta/")
        self.df = pd.DataFrame(["123", "456"])

    def tearDown(self):
        self.input_.recycle()
        pass

    def test_remote_sftp_connector__auth_fail(self):
        try:
            con = RemoteSFTPConnector('localhost')
        except paramiko.ssh_exception.SSHException as e:
            pass
        pass

    def test_datamanager__normal(self):
        self.input_.meta_workspace.dump(self.df, "123456.json")

        self.assertTrue(os.path.exists(self.root_folder + "/meta/123456.json"))
