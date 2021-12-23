import sys
import traceback
import random
import pandas as pd

from sklearn import linear_model
from sklearn.svm import SVR

from lib.db import mongo
from lib.dataframe import generate_dataframe
from lib.helpers.model_helper import ModelHelper

from lib.v1.regressors.base_non_linear_regressor import BaseNonLinearRegressor

class SVRRegressor(BaseNonLinearRegressor):
    def train(self, request):
        model = SVR(kernel='poly', C=100, gamma='auto', degree=3, epsilon=.1, coef0=1)
        # model = SVR(kernel='linear', C=100, gamma='auto')
        # model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)

        return BaseNonLinearRegressor.train(self, model, request)
