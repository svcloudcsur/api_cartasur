# ------------------------------------------------------------------------------
#
#  Base Regressor
#
# ------------------------------------------------------------------------------

import sys
import traceback
import random
import pandas as pd

from lib.db import mongo
from lib.dataframe import generate_dataframe
from lib.helpers.model_helper import ModelHelper
from lib.v1.variables import Variables

class BaseRegressor():
    def train(self, model, request):
        try:
            clientes = []
            for cliente in mongo.db.clientes.find(no_cursor_timeout=True):
                clientes.append(cliente)

            # Number of clients in the batch
            BATCH_SIZE = int(request.args.get("batch_size")) or 5000
            print("[ii] Using a BATCH_SIZE of {} clients".format(BATCH_SIZE))
            batch_count = 1
            client_count = 0        # Number of clients in the batch upto now
            X = pd.DataFrame()      # X current dataframe
            y = pd.DataFrame()      # Y current dataframe

            for cliente in clientes:
                client_count += 1

                if(client_count % BATCH_SIZE == 0):
                    print("[ii] Partial Fit of {} clients".format(client_count))

                    model.partial_fit(X, y.values.ravel()) # https://stackoverflow.com/questions/34165731/a-column-vector-y-was-passed-when-a-1d-array-was-expected
                    ModelHelper.save(model)

                    # ---------------------------------------------------------
                    #  RESET everything for the next batch
                    # ---------------------------------------------------------
                    client_count = 1
                    batch_count += 1

                    result = generate_dataframe(credito_df, cliente_df, cuotas_df, pagos_df)
                    X = result[ Variables.X_independent_variables() ]
                    y = result[ Variables.y_dependent_variable() ]

                else:
                    creditos = mongo.db.creditos.find({"creditos_ID_CLIENTE": cliente['clientes_ID_CLIENTE']}, no_cursor_timeout=True)

                    print("[ii] Added {} clients to the batch # {}".format(client_count % BATCH_SIZE, batch_count))

                    for credito in creditos:
                        id_credito = credito['creditos_ID_CREDITO']
                        cliente_df = pd.DataFrame(cliente, index=[0])
                        credito_df = pd.DataFrame(credito, index=[0])
                        cuotas_df = pd.DataFrame(list(mongo.db.cuotas.find({"ID_CREDITO": id_credito}, no_cursor_timeout=True)))
                        pagos_df = pd.DataFrame(list(mongo.db.pagos.find({"pagos_ID_CREDITO": id_credito}, no_cursor_timeout=True)))

                        result = generate_dataframe(credito_df, cliente_df, cuotas_df, pagos_df)

                        # -- REMOVE THIS WHEN POSSIBLE --
                        # if(result['credito_score'][0] <= 0):
                        #     continue

                        current_X = result[ Variables.X_independent_variables() ]
                        current_y = result[ Variables.y_dependent_variable() ]

                        X = X.append(current_X)
                        y = y.append(current_y)

            reminding_clients = client_count % BATCH_SIZE

            if reminding_clients > 0:
                print("[ii] Flushing {} clients".format(reminding_clients))
                model.partial_fit(X, y.values.ravel()) # https://stackoverflow.com/questions/34165731/a-column-vector-y-was-passed-when-a-1d-array-was-expected
        except Exception as e:
            traceback.print_exc(file=sys.stdout)

        return model
