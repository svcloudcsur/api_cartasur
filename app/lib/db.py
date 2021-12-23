import os

from flask_pymongo import PyMongo

mongo_settings_uri = "mongodb://{user}:{password}@{host}:27017/{dbname}?authSource=admin".format(
  user=os.getenv('MONGO_INITDB_ROOT_USERNAME'),
  password=os.getenv('MONGO_INITDB_ROOT_PASSWORD'),
  dbname=os.getenv('MONGO_INITDB_DATABASE'),
  host=os.getenv('MONGO_INITDB_HOSTNAME'),
  port="27017"
)

mongo = PyMongo()
