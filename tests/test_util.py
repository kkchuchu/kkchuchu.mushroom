import unittest

import pandas as pd

from scrd_tool import util


class TestUM(unittest.TestCase):
     
    def setup(self):
        self.df = pd.DataFrame(data=[])
        print ("TestUM:setup() before each test method")
        
    def test_numbers_5_6(self):
        assert 5 * 6 == 30
        
    def test_count_by__normal(self):
        util.count_by(self.df, by=[])
        pass