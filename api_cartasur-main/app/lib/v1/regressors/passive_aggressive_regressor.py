# ------------------------------------------------------------------------------
# Passive Aggressive Regressor
#
# Since the data provided by API Cartasur is too big, we have to move to
# a model that can be trained in chunks like the Stochastic Gradient Descent.
# ------------------------------------------------------------------------------

import sys
import traceback
import random
import pandas as pd

from sklearn import linear_model
from sklearn.linear_model import PassiveAggressiveRegressor

from lib.db import mongo
from lib.dataframe import generate_dataframe
from lib.helpers.model_helper import ModelHelper

from lib.v1.regressors.base_regressor import BaseRegressor

class PAR(BaseRegressor):
    def train(self, request):
        model = PassiveAggressiveRegressor()
        return BaseRegressor.train(self, model, request)
