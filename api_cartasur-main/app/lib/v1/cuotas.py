import sys
import traceback
import numpy as np

from flask import jsonify
from dateutil.parser import parse

from lib.db import mongo
from lib.v1.document import Document
from lib.tools import parse_date
from lib.tools import round_values

class Cuotas(Document):
    COLLECTION_NAME='cuotas'
    #  Mostrar todos
    # ----------------------------------------------------------------------
    def get(self):
        # return [doc for doc in mongo.db.cuotas.find({}, {"_id":0})]
        return {"cantidad_cuotas" : mongo.db.cuotas.count()}

    #  Normalization for Cuotas
    # ----------------------------------------------------------------------
    def normalize(self, cuotas_df):
        try:
            parse_date(cuotas_df, 'FVTO')
            round_values(cuotas_df, 'CAPITAL', 100)
            round_values(cuotas_df, 'INTERES', 100)
            return cuotas_df
        except Exception as e:
            traceback.print_exc(file=sys.stdout)

    #  Updates the collection
    # ----------------------------------------------------------------------
    def update_collection(self, df):
        chunks = 200000
        counter = 0
        print("[ii] Using chunks of {} elements".format(chunks))
        Document.update_collection(self, df)
        for k,g in df.groupby(np.arange(len(df))//chunks):
            mongo.db.cuotas.insert_many(g.to_dict('records'))
            counter += chunks
            print("  [ii] {} elements inserted".format(counter))

    #  Create an index
    # ----------------------------------------------------------------------
    def create_index(self):
        mongo.db.cuotas.create_index("ID_CREDITO")
