"""
pandas introduction: https://pandas.pydata.org/pandas-docs/stable/dsintro.html
"""

class Summary(object):

    def __init__(self, df):
        # df is a pandas.core.frame.DataFrame
        self._frame = df
    
    def column_type(self):
        return df.dtype

    def describe(self, column_name):
        dr[column_name].describe()

    def show(self, column_name):
        pass

    def describe_all(self):
        dr.describe(include='all')

