import numpy as np

from dateutil.parser import parse

from lib.v1.document import Document

from lib.db import mongo
from lib.tools import parse_date
from lib.tools import parse_float
from lib.tools import rename_columns

class Pagos(Document):
    COLLECTION_NAME = 'pagos'
    #  Mostrar todos
    # ----------------------------------------------------------------------
    def get(self):
        # return [doc for doc in mongo.db.pagos.find({}, {"_id":0})]
        return {"cantidad_pagos" : mongo.db.pagos.count()}

    #  Normalization for Pagos
    # ----------------------------------------------------------------------
    def normalize(self, pagos_df):
        parse_date(pagos_df, 'FPAGO')
        parse_float(pagos_df, 'CAPITAL')
        parse_float(pagos_df, 'INTERES')
        rename_columns(pagos_df, 'pagos')
        return pagos_df

    #  Updates the collection
    # ----------------------------------------------------------------------
    def update_collection(self, df):
        chunks = 200000
        counter = 0
        print("[ii] Using chunks of {} elements".format(chunks))
        Document.update_collection(self, df)
        for k,g in df.groupby(np.arange(len(df))//chunks):
            mongo.db.pagos.insert_many(g.to_dict('records'))
            counter += chunks
            print("  [ii] {} elements inserted".format(counter))

    #  Create an index
    # ----------------------------------------------------------------------
    def create_index(self):
        mongo.db.pagos.create_index("pagos_ID_CREDITO")
