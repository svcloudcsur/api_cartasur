import pickle
import pandas as pd

from flask import jsonify
from lib.db import mongo

from lib.v1.variables import Variables

class Predictor:
    def post(self, request):
        serialized = list(mongo.db.model.find({}))[0]
        model = pickle.loads(serialized["model"])

        # Check 'variables' module to see which variables were used to train
        X_input = pd.DataFrame(request.args, index=[0])
        y_pred = model.predict(X_input)

        return {"score": y_pred[0]}
