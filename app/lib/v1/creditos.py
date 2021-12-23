import numpy as np

from dateutil.parser import parse
from lib.v1.document import Document
from lib.db import mongo
from lib.tools import *

class Creditos(Document):
    COLLECTION_NAME='creditos'

    #  Mostrar todos
    # ----------------------------------------------------------------------
    def get(self):
        # return [doc for doc in mongo.db.creditos.find({}, {"_id":0})]
        return {"cantidad_creditos" : mongo.db.creditos.count()}

    #  Normalization for creditos
    # ----------------------------------------------------------------------
    def normalize(self, creditos_df):
        for col in ['TDOC', 'NDOC','PKEY_JOB', 'PAR_KEY']:
            if col in creditos_df.columns:
                drop_column(creditos_df, col)

        for col in ['FECHAINFORME', 'FLIQUIDACION']:
            if col in creditos_df.columns:
                parse_date(creditos_df, col)

        parse_float(creditos_df, 'MONTO')
        parse_categories(creditos_df, 'SUCURSAL')
        parse_categories(creditos_df, 'NOMBRE')
        parse_yes_no(creditos_df, 'RECIBO')
        parse_categories(creditos_df, 'CLASE_PLAN')
        parse_categories(creditos_df, 'siisa_subsectorLaboral')
        parse_categories(creditos_df, 'siisa_sectorLaboral')
        round_values(creditos_df, 'siisa_ingreso', 1000)
        round_values(creditos_df, 'siisa_compromiso', 100)
        round_values(creditos_df, 'siisa_montoMorasBCRA', 100)
        parse_int(creditos_df, 'siisa_relDepMeses')
        round_values(creditos_df, 'veraz_score', 10)
        round_values(creditos_df, 'siisa_sesModelo', 5)
        round_values(creditos_df, 'siisa_consultasAno', 1)
        parse_categories(creditos_df, 'siisa_sectorLaboral')
        round_values(creditos_df, 'siisa_ingreso', 1000)
        round_values(creditos_df, 'siisa_compromiso', 100)
        parse_int(creditos_df, 'siisa_maxBCRA24m')
        parse_int(creditos_df, 'siisa_score')
        parse_categories(creditos_df, 'siisa_scorePoblacion')
        parse_int(creditos_df, 'siisa_maxBCRA12m')
        parse_int(creditos_df, 'siisa_cantMoras')
        parse_int(creditos_df, 'siisa_maxBCRA6m')
        parse_int(creditos_df, 'siisa_consultasSeisMeses')
        parse_int(creditos_df, 'siisa_sesCat')
        parse_int(creditos_df, 'siisa_consultasDosAno')
        parse_int(creditos_df, 'siisa_consultasTresMeses')
        parse_int(creditos_df, 'siisa_consultasMes')
        rename_columns(creditos_df, 'creditos')

        return creditos_df


    #  Updates the collection
    # ----------------------------------------------------------------------
    def update_collection(self, df):
        chunks = 200000
        print("[ii] Using chunks of {} elements".format(chunks))
        Document.update_collection(self, df)
        for k,g in df.groupby(np.arange(len(df))//chunks):
            mongo.db.creditos.insert_many(g.to_dict('records'))

    #  Create an index
    # ----------------------------------------------------------------------
    def create_index(self):
        mongo.db.creditos.create_index("creditos_ID_CLIENTE")
