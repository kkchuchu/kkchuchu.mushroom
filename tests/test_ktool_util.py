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

from ktool.util import time_converter


class TestKToolUtil(unittest.TestCase):
    
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
        pass

    def setUp(self):
        pass
    
    def test_time_converter__normal(self):
        d = time_converter("2020-04-05T10:00:00.000Z")
        e_d = datetime.datetime(year=2020, month=4, day=5, hour=10, tzinfo=pytz.utc)
        self.assertEqual(e_d, d)