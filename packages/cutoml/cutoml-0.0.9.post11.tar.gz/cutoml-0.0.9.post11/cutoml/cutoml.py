"""
CutoML - A lightweight automl framework for classification and regression tasks.

Copyright (C) 2021 Omkar Udawant

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from cutoml.utils import regression_metrics
from cutoml.utils import classification_metrics
from cutoml.utils import timer
from cutoml.config import Classifiers
from cutoml.config import Regressors

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

from pathos.multiprocessing import ProcessingPool as Pool
from pathos import multiprocessing

import numpy as np
import time
import json
import tqdm
import warnings


class CutoClassifier:
    def __init__(self, k_folds=3, n_jobs=2, verbose=0):
        self.models = Classifiers(
            k_folds=k_folds, n_jobs=n_jobs, verbose=verbose)
        self.models = self.models.models
        self.best_estimator = None
        self.n_jobs = n_jobs

    def _model_fitter(self, model, X, y):
        clfs = list()
        try:
            clf = Pipeline([
                ('classification_model', model)
            ])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                clf = clf.fit(X, y)
                clfs.append(clf)
            return clf
        except Exception as e:
            pass

    def fit(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=0
        )

        start_time = time.time()
        pool = Pool()
        try:
            *trained_pipelines, = tqdm.tqdm(pool.map(lambda x: self._model_fitter(x,
                                                                                  X_train,
                                                                                  y_train),
                                                     self.models)
                                            )
            end_time = time.time()
        finally:
            pool.close()
            pool.join()
        # print(timer(start=start_time, end=end_time))

        trained_models = dict()
        for pipeline in trained_pipelines:
            if pipeline:
                try:
                    pred = pipeline.predict(X_test)
                    acc, f1, prec, recall, roc_auc = classification_metrics(
                        y_true=y_test, y_pred=pred
                    )
                    trained_models[f1] = pipeline
                except Exception as e:
                    pass
        if trained_models:
            self.best_estimator = max(
                sorted(trained_models.items(), reverse=True))[1]
            return self
        else:
            raise RuntimeError('Could not find best estimator.')

    def predict(self, X):
        if not self.best_estimator:
            raise RuntimeError(
                'Models not fit yet, please call object.fit() method first.')
        prediction = self.best_estimator.predict(X)
        return prediction

    def predict_proba(self, X):
        if not self.best_estimator:
            raise RuntimeError(
                'Models not fit yet, please call object.fit() method first.')
        prediction_probablity = self.best_estimator.predict_proba(X)
        return prediction_probablity

    def score(self, X, y):
        if not self.best_estimator:
            raise RuntimeError(
                'Models not fit yet, please call object.fit() method first.')
        pred = self.best_estimator.predict(X)
        accuracy, f1, precision, recall, roc_auc_ = classification_metrics(
            y_true=y, y_pred=pred
        )
        scores = {
            "Accuracy": accuracy,
            "F1 score": f1,
            "Precision": precision,
            "Recall": recall,
            "ROC_AUC_score": roc_auc_,
        }
        return json.dumps(scores, sort_keys=True)


class CutoRegressor:
    def __init__(self, k_folds=3, n_jobs=2, verbose=0):
        self.models = Regressors(
            k_folds=k_folds, n_jobs=n_jobs, verbose=verbose)
        self.models = self.models.models
        self.best_estimator = None
        self.n_jobs = n_jobs

    def _model_fitter(sef, model, X, y):
        try:
            rgr = Pipeline([
                ('regression_model', model)
            ])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                rgr = rgr.fit(X, y)
            return rgr
        except Exception as e:
            pass

    def fit(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=0
        )
        start_time = time.time()
        pool = Pool()
        try:
            *trained_pipelines, = tqdm.tqdm(pool.map(lambda x: self._model_fitter(x,
                                                                                  X_train,
                                                                                  y_train),
                                                     self.models)
                                            )
            end_time = time.time()
        finally:
            pool.close()
            pool.join()
        # print(timer(start=start_time, end=end_time))

        trained_models = dict()
        for pipeline in trained_pipelines:
            if pipeline:
                try:
                    pred = pipeline.predict(X_test)
                    r2, mape, mse, mae = regression_metrics(y_true=y_test,
                                                            y_pred=pred)
                    trained_models[r2] = pipeline
                except Exception as e:
                    pass
        if trained_models:
            self.best_estimator = max(
                sorted(trained_models.items(), reverse=True))[1]
            return self
        else:
            raise RuntimeError('Could not find best estimator.')

    def predict(self, X):
        if not self.best_estimator:
            raise RuntimeError(
                'Models not fit yet, please call object.fit() method first.')
        prediction = self.best_estimator.predict(X)
        return prediction

    def score(self, X, y):
        if not self.best_estimator:
            raise RuntimeError(
                'Models not fit yet, please call object.fit() method first.')
        pred = self.best_estimator.predict(X)
        r2, mape, mse, mae = regression_metrics(y_true=y, y_pred=pred)
        scores = {"R2 score": r2, "MAPE": mape, "MSE": mse, "MAE": mae}
        return json.dumps(scores, sort_keys=True)
