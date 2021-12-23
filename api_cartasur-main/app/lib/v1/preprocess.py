import sys
import traceback
import pandas as pd

from flask import jsonify
from lib.db import mongo

from lib.dataframe import generate_dataframe
from lib.v1.variables import Variables

class Preprocess:
    # ---------------------------------------------------------------------
    #  Process the put request
    # ---------------------------------------------------------------------
    def put(self, request):
        try:
            independent_variables = Variables.X_independent_variables()
            dependent_variable = Variables.y_dependent_variable()

            clientes = []
            for cliente in mongo.db.clientes.find(no_cursor_timeout=True):
                clientes.append(cliente)

            BATCH_SIZE = int(request.args.get("batch_size")) or 200
            limit = request.args.get("limit") or None
            client_count = 0

            print("[ii] Using a BATCH_SIZE of {} clients".format(BATCH_SIZE))

            if(request.args.get('drop_collection') == 'true'):
                print('[ww] dropping collection preprocess')
                mongo.db.drop_collection('preprocess')
                mongo.db.create_collection('preprocess')

            for cliente in clientes:
                client_count += 1

                creditos = mongo.db.creditos.find({"creditos_ID_CLIENTE": cliente['clientes_ID_CLIENTE']}, no_cursor_timeout=True)
                for credito in creditos:
                    id_credito = credito['creditos_ID_CREDITO']

                    cliente_df = pd.DataFrame(cliente, index=[0])
                    credito_df = pd.DataFrame(credito, index=[0])
                    cuotas_df = pd.DataFrame(list(mongo.db.cuotas.find({"ID_CREDITO": id_credito}, no_cursor_timeout=True)))
                    pagos_df = pd.DataFrame(list(mongo.db.pagos.find({"pagos_ID_CREDITO": id_credito}, no_cursor_timeout=True)))

                    result = generate_dataframe(credito_df, cliente_df, cuotas_df, pagos_df)

                    X = result[ independent_variables ]
                    y = result[ dependent_variable ]

                    mongo.db.preprocess.insert_one({'X': X.values.flatten().tolist(), 'y' : float(result[dependent_variable].iloc[0])})

                if limit != None and client_count % int(limit) == 0:
                    print("[WARNING] >>> A limit was set and ONLY {} clients were processed".format(client_count))
                    break

                if client_count % BATCH_SIZE == 0:
                    print("[ii] {} clients were stored".format(client_count))

            return "Los datos han sido preprocessados"
        except:
            traceback.print_exc(file=sys.stdout)
            return jsonify("Ha ocurrido un problema preprocesando los datos"), 500
