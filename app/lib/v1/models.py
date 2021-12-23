import sys
import pickle
import traceback

from lib.db import mongo
from lib.tools import *
from lib.dataframe import *
from lib.helpers.model_helper import ModelHelper

from lib.v1.regressors.linear_regressor import LinearRegressor
from lib.v1.regressors.stochastic_gradient_regressor import StochasticGradientRegressor
from lib.v1.regressors.passive_aggressive_regressor import PAR
from lib.v1.regressors.multi_layer_perceptron_regressor import MultiLayerPerceptronRegressor
from lib.v1.regressors.svr_regressor import SVRRegressor
from lib.v1.regressors.p_linear_regressor import PLinearRegressor
from lib.v1.regressors.p_random_forest import PRandomForest

class Models:
    COLLECTION_NAME='model'

    # ---------------------------------------------------------------------
    #  Process the put request
    # ---------------------------------------------------------------------
    def put(self, request):
        model = self.get_model(request)
        try:
            trained_model = model.train(request)
            ModelHelper.save(trained_model)

            return "El modelo ha sido entrenado correctamente utilizando {}".format(model.__class__.__name__)
        except:
            if model.__class__.__name__ == 'NoneType':
                return "El modelo elegido no existe"
            else:
                traceback.print_exc(file=sys.stdout)
                return "Ha habido un problema entrenando el modelo con {}".format(model.__class__.__name__)

    # ---------------------------------------------------------------------
    #  Gets the model based on the parameters
    # ---------------------------------------------------------------------
    def get_model(self, request):
        model_type = request.args.get('model_type')
        print("[ii] Learning using {} model".format(model_type))
        if(model_type == "linear_regression"):
            return LinearRegressor()
        elif(model_type == "sgd_regression"):
            return StochasticGradientRegressor()
        elif(model_type == "par_regression"):
            return PAR()
        elif(model_type == "mlp_regression"):
            return MultiLayerPerceptronRegressor()
        elif(model_type == "svr_regression"):
            return SVRRegressor()
        elif(model_type == "p_linear_regression"):
            return PLinearRegressor()
        elif(model_type == "p_random_forest_regression"):
            return PRandomForest()
