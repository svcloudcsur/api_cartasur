import sys
import traceback

from flask import jsonify
from lib.db import mongo
from datetime import datetime

class Variables:
    def get(self):
        return [doc for doc in mongo.db.selected_variables.find({}, {"_id":0})]

    def post(self, request):
        try:
            X = request.args.get('X').split(',')
            y = request.args.get('y').split(',')
            date_now = datetime.now().isoformat()

            mongo.db.drop_collection('selected_variables')
            mongo.db.create_collection('selected_variables', {})
            mongo.db.selected_variables.insert_one({'X':X, 'y':y, 'date': date_now})
            return {
                "result": "SUCCESS",
                "X": X,
                "y": y,
                "date": date_now
            }
        except:
            traceback.print_exc(file=sys.stdout)
            return jsonify("Ha ocurrido un problema seteando las variables"), 500

    def X_independent_variables():
        return mongo.db.selected_variables.find()[0]['X']

    def y_dependent_variable():
        return mongo.db.selected_variables.find()[0]['y']
