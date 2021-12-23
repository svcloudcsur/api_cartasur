# -------------------------------------------------------------------------
#   DO NOT USE THIS ONE, it is *VERY* innacurate
# -------------------------------------------------------------------------
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from lib.db import mongo
from lib.dataframe import generate_dataframe
from lib.v1.variables import Variables

class LinearRegressor:
    def train(self, request):
        percentage = request.args.get('test_percentage')

        if(percentage == None):
            percentage = 0.2
        else:
            percentage = float(int(request.args.get('test_percentage'))) / 100.0

        cuotas_df = pd.DataFrame(list(mongo.db.cuotas.find({})))
        clientes_df = pd.DataFrame(list(mongo.db.clientes.find({})))
        creditos_df = pd.DataFrame(list(mongo.db.creditos.find({})))
        pagos_df = pd.DataFrame(list(mongo.db.pagos.find({})))

        result = generate_dataframe(creditos_df, clientes_df, cuotas_df, pagos_df)

        X = result [ Variables.X_independent_variables() ]
        y = result[ Variables.y_dependent_variable() ]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percentage, random_state=0)

        model = LinearRegression()

        # Entrenamiento
        model.fit(X_train, y_train)

        return model
