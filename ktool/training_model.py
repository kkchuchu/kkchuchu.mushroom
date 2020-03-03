from autosklearn import regression
from sklearn import model_selection

from .util import BaseConfig


class BaseModel(object):

    def __init__(self, config=None, time_left_for_this_task=120, per_run_time_limit=30, train_test_split=False,
                 dataset_name="ktool", default_project_name="default_project", *args, **kwargs):
        """[summary]

        Arguments:
            feature_types {[type]} -- Like this feature_types = (['numerical'] * 1)

        Keyword Arguments:
            time_left_for_this_task {int} -- [description] (default: {120})
            per_run_time_limit {int} -- [description] (default: {30})
            train_test_split {bool} -- [description] (default: {False})
        """
        # self._feature_types = feature_types
        self._time_left_for_this_task = time_left_for_this_task
        self._per_run_time_limit = per_run_time_limit
        self._random_state = 1
        self._train_test_split = train_test_split
        self._dataset_name = dataset_name
        if config is None:
            self.config = BaseConfig('./output/', default_project_name)
        else:
            self.config = config
        self._tmp_folder = self.config.get_project_tmp_folder()
        self._output_folder = self.config.get_project_base_folder()
        print("temp folder: %r", self._tmp_folder)
        print("output folder: %r", self._output_folder)
        
        self.model = regression.AutoSklearnRegressor(
            time_left_for_this_task=self._time_left_for_this_task,
            per_run_time_limit=self._per_run_time_limit,
            tmp_folder=self._tmp_folder,
            output_folder=self._output_folder,
            delete_tmp_folder_after_terminate=True,
            resampling_strategy='cv',
            resampling_strategy_arguments={'folds': 5},
        )

    def run(self): 
        #TBD: config, feature_types,
        # self.predict(x, y)
        pass
        
    def score(self, X, y):
        return self.model.score(X, y)
    
    def get_params(self, deep=True):
        return self.model.get_params(deep=deep)
        
    def fit(self, x, y):
        X_train, y_train = x, y
        r = self.model.fit(X_train, y_train, dataset_name=self._dataset_name)
        print(self.model.show_models())
        return r
    
    def refit(self, X, y):
        return self.model.refit(X, y)
            
    def predict(self, x):
        return self.model.predict(x)

    def evaluate(self, x, y):
        if self._train_test_split:
            X_train, X_test, y_train, y_test = \
                model_selection.train_test_split(
                    x, y, random_state=self._random_state)
        else:
            X_train, X_test, y_train, y_test = x, None, y, None
        if X_test is not None:
            predictions = self.model.predict(X_test)
            # print("R2 score:", sklearn.metrics.r2_score(y_test, predictions))