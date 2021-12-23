# ------------------------------------------------------------------------------
#
#  Stochastic Gradient Descent Regressor
#
# ------------------------------------------------------------------------------

import sys
import traceback
import random
import pandas as pd

from sklearn import linear_model
from sklearn.linear_model import SGDRegressor

from lib.db import mongo
from lib.dataframe import generate_dataframe
from lib.helpers.model_helper import ModelHelper
from lib.v1.regressors.base_regressor import BaseRegressor

class StochasticGradientRegressor(BaseRegressor):
    def train(self, request):
        model = SGDRegressor()
        return BaseRegressor.train(self, model, request)
