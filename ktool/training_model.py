from autosklearn import regression
from sklearn import model_selection


class BaseModel(object):

    def __init__(self, config, feature_types, time_left_for_this_task=120, per_run_time_limit=30, train_test_split=False,
                 dataset_name="ktool"):
        """[summary]

        Arguments:
            feature_types {[type]} -- Like this feature_types = (['numerical'] * 1)

        Keyword Arguments:
            time_left_for_this_task {int} -- [description] (default: {120})
            per_run_time_limit {int} -- [description] (default: {30})
            train_test_split {bool} -- [description] (default: {False})
        """
        self._feature_types = feature_types
        self._time_left_for_this_task = time_left_for_this_task
        self._per_run_time_limit = per_run_time_limit
        self._random_state = 1
        self._train_test_split = train_test_split
        self._dataset_name = dataset_name
        self.config = config
        self._tmp_folder = self.config.get_project_tmp_folder()
        self._output_folder = self.config.get_project_base_folder()

    def run(self):
        self.predict(x, y)

    def predict(self, x, y):
        if self._train_test_split:
            X_train, X_test, y_train, y_test = \
                model_selection.train_test_split(
                    x, y, random_state=self._random_state)
        else:
            X_train, X_test, y_train, y_test = x, None, y, None
        automl = regression.AutoSklearnRegressor(
            time_left_for_this_task=self._time_left_for_this_task,
            per_run_time_limit=self._per_run_time_limit,
            tmp_folder=self._tmp_folder,
            output_folder=self._output_folder,
        )
        automl.fit(X_train, y_train, dataset_name=self._dataset_name,
                   feat_type=self._feature_types)
        print(automl.show_models())
        
        if X_test is not None:
            predictions = automl.predict(X_test)
            # print("R2 score:", sklearn.metrics.r2_score(y_test, predictions))
