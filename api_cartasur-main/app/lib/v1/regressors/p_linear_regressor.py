import sys
import numpy
import pandas as pd

from sklearn.ensemble import RandomForestRegressor # XXX

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from lib.db import mongo
from lib.dataframe import generate_dataframe
from lib.v1.variables import Variables

class PLinearRegressor:
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
        variables = set(request.args.get('X_independent_variables_to_use').split(','))

        i = 0
        required_cols = []
        for col in columns:
            if col in variables:
                required_cols.append(i)
            i += 1

        count = 0
        for preprocess in mongo.db.preprocess.find(no_cursor_timeout=True):
            # -------------------------------------------------------------
            #  Select columns based on user request
            # -------------------------------------------------------------
            X = X.append([numpy.array(preprocess['X'])[required_cols].tolist()])
            y = y.append([preprocess['y']])

            count += 1

            if((limit != 0) and (count % limit == 0)):
                break

            if count % 250 == 0:
                print("[ii] {} datos agregados".format(count))
                sys.stdout.flush()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percentage, random_state=0)

        model = LinearRegression()

        # Entrenamiento
        model.fit(X_train, y_train)

        model_rf = RandomForestRegressor(max_depth=20, random_state=413) # XXX - remove me [esto tiene que moverse a su propio regressor]
        model_rf.fit(X_train, y_train.values.ravel()) # XXX - remove me [esto hay que moverlo a su propio regressor]

        y_pred = model.predict(X_test)
        y_pred_rf = model_rf.predict(X_test)

        from sklearn.metrics import r2_score
        r2_score(y_test, y_pred)
        r2_score(y_test, y_pred_rf)

        # import ipdb; ipdb.set_trace()

        print("[ii] ENTRENADO! utilizando {} datos".format(count))
        sys.stdout.flush()

        return model
