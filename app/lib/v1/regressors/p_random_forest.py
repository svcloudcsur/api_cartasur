import sys
import numpy
import pandas as pd

from sklearn.ensemble import RandomForestRegressor # XXX

from sklearn.model_selection import train_test_split

from lib.db import mongo
from lib.dataframe import generate_dataframe
from lib.v1.variables import Variables

class PRandomForest:
    def train(self, request):
        percentage = request.args.get('test_percentage')
        limit = int(request.args.get('limit') or "0")

        if(percentage == None):
            percentage = 0.2
        else:
            percentage = float(int(request.args.get('test_percentage'))) / 100.0

        X = pd.DataFrame()
        y = pd.DataFrame()

        # -----------------------------------------------------------------
        #  Get the indexes we want to train based on the user request
        # -----------------------------------------------------------------
        columns = Variables.X_independent_variables()
        variables = request.args.getlist('variable')

        selected_variables = mongo.db.selected_variables.find_one()
        required_columns = []
        for var in request.args.getlist('variable'):
            col_number = 0
            for model_var in selected_variables['X']:
                if(model_var == var):
                    required_columns.append(col_number)
                col_number += 1

        count = 0
        for preprocess in mongo.db.preprocess.find(no_cursor_timeout=True):
            # -------------------------------------------------------------
            #  Select columns based on user request
            # -------------------------------------------------------------
            X = X.append([numpy.array(preprocess['X'])[required_columns].tolist()])
            y = y.append([preprocess['y']])

            count += 1

            if((limit != 0) and (count % limit == 0)):
                break

            if count % 250 == 0:
                print("[ii] {} datos agregados".format(count))
                sys.stdout.flush()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percentage, random_state=0)

        model = RandomForestRegressor(max_depth=20, random_state=413)
        model.fit(X_train, y_train.values.ravel())

        from sklearn.metrics import r2_score
        y_pred = model.predict(X_test)

        print("[ii] ENTRENADO! utilizando {} datos / el r2_score={}".format(count, r2_score(y_test, y_pred)))
        sys.stdout.flush()

        return model
