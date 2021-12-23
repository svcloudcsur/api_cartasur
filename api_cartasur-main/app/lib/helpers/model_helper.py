import pickle
from lib.db import mongo

class ModelHelper:
    def save(trained_model):
        mongo.db.drop_collection('model')
        mongo.db.create_collection('model', {})
        mongo.db.model.insert_one({"model" : pickle.dumps(trained_model)})
