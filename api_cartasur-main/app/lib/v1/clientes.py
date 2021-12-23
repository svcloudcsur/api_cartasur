import numpy as np

from dateutil.parser import parse
from lib.db import mongo
from lib.v1.document import Document
from lib.tools import parse_date
from lib.tools import round_values
from lib.tools import parse_categories
from lib.tools import parse_int
from lib.tools import rename_columns
from lib.tools import drop_column

class Clientes(Document):
    COLLECTION_NAME='clientes'

    #  Mostrar todos
    # ----------------------------------------------------------------------
    def get(self):
        #return [doc for doc in mongo.db.clientes.find({}, {"_id":0})]
        return {"cantidad_clientes" : mongo.db.clientes.count()}

    #  Normalization for Clientes
    # ----------------------------------------------------------------------
    def normalize(self, clientes_df):
        for col in ['TDOC', 'NROC','FECHA_ALTA_LABORAL','SUCURSAL','COD_POSTAL_PER','PROVINCIA_PER']:
            if col in clientes_df.columns:
                drop_column(clientes_df, col)

        parse_date(clientes_df, 'FALTA')
        parse_date(clientes_df, 'FNAC')
        round_values(clientes_df, 'INGRESO_NETO', 1000)
        parse_categories(clientes_df, 'TIPOLABORAL')
        parse_categories(clientes_df, 'METAL')
        parse_int(clientes_df, 'OPERACIONES')
        parse_int(clientes_df, 'REFINES')
        parse_int(clientes_df, 'PEOR_ATRASO_HIST')
        parse_int(clientes_df, 'JUICIOS_CANCELADOS')
        parse_categories(clientes_df, 'APTO_VENTA_EN_CAJA')
        rename_columns(clientes_df, 'clientes')

        return clientes_df


    #  Updates the collection
    # ----------------------------------------------------------------------
    def update_collection(self, df):
        chunks = 200000
        print("[ii] Using chunks of {} elements".format(chunks))
        Document.update_collection(self, df)
        for k,g in df.groupby(np.arange(len(df))//chunks):
            mongo.db.clientes.insert_many(g.to_dict('records'))
