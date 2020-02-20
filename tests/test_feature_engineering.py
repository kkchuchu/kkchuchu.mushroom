import unittest

import pandas as pd
import numpy as np
from scrd_tool import feature_engineering



class TestUM(unittest.TestCase):
     
    def setup(self):
        index = pd.date_range("1 1 2000", periods=100,
                      freq="m", name="date")

        data = np.random.randn(100, 4).cumsum(axis=0)
        self.df = pd.DataFrame(data, index, ["a", "b", "c", "d"])
        print ("TestUM:setup() before each test method")
        
    def test_numbers_5_6(self):
        assert 5 * 6 == 30
        
    def test_count_by__normal(self):
        pass
    
    def test_cont2cont_point__normal(self):
        feature_engineering.cont2cont_point(self.df)