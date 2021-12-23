import sys
import traceback
import random
import pandas as pd

from sklearn import linear_model
from sklearn.neural_network import MLPRegressor

from lib.db import mongo
from lib.dataframe import generate_dataframe
from lib.helpers.model_helper import ModelHelper

from lib.v1.regressors.base_regressor import BaseRegressor

class MultiLayerPerceptronRegressor(BaseRegressor):
    def train(self, request):
        # -----
        # Hyper Parameters
        # https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html#sklearn.neural_network.MLPRegressor
        # -----
        #  hidden_layer_sizes=100,
        #  activation='relu', *,
        #  solver='adam',
        #  alpha=0.0001,
        #  batch_size='auto',
        #  learning_rate='constant',
        #  learning_rate_init=0.001,
        #  power_t=0.5,
        #  max_iter=200,
        #  shuffle=True,
        #  random_state=None,
        #  tol=0.0001,
        #  verbose=False,
        #  warm_start=False,
        #  momentum=0.9,
        #  nesterovs_momentum=True,
        #  early_stopping=False,
        #  validation_fraction=0.1,
        #  beta_1=0.9,
        #  beta_2=0.999,
        #  epsilon=1e-08,
        #  n_iter_no_change=10,
        #  max_fun=15000
        model = MLPRegressor()
        return BaseRegressor.train(self, model, request)
