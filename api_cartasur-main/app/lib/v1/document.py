import sys
import traceback
import pandas as pd
from lib.db import mongo
from flask import jsonify

class Document:
    SEPARATOR = '|'
    COLLECTION_NAME = 'undefined'
    ENCODING='iso-8859-1'

    #  Updates the collection
    # ---------------------------------------------------------------------
    def update(self, file):
        try:
            print("[ii] Reading CSV")
            df = pd.read_csv(file, sep=self.SEPARATOR, encoding=self.ENCODING)
            print("[ii] Starting normalization")
            df = self.normalize(df)
            print("[ii] Updating")
            self.create_or_update_collection(df)

            return True
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return False

    #  Normalizes the collection
    #  Dervied classes must redefine this to normalize data
    # ---------------------------------------------------------------------
    def normalize(self, df):
        return df

    #  TO BE REDEFINED in derived classes
    # ---------------------------------------------------------------------
    def update_collection(self, df):
        return df

    #  TO BE REDEFINED (if needed) in derived classes
    def create_index(self):
        return True

    #  Creates/Updates the collection [ IT IS DESTRUCTIVE ]
    # ---------------------------------------------------------------------
    def create_or_update_collection(self, df):
        print("[INFO] drop {} collection".format(self.__class__.__name__))
        mongo.db.drop_collection(self.COLLECTION_NAME)
        print("[INFO] create {} collection".format(self.__class__.__name__))
        mongo.db.create_collection(self.COLLECTION_NAME, {})
        print("[INFO] update {} collection".format(self.__class__.__name__))
        self.update_collection(df)
        print("[INFO] create {} index".format(self.__class__.__name__))
        self.create_index()
