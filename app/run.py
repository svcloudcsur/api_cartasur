import os
from flask import Flask, jsonify

from api.v1 import api_v1
from lib.db import mongo, mongo_settings_uri
from lib.ping import pong

app = Flask(__name__)

#  Configurations
# -------------------------------------------------------------------
app.config['MONGO_URI']     = mongo_settings_uri
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')

#  Mongo
# -------------------------------------------------
mongo.init_app(app)

#  Routes
# -------------------------------------------------
@app.route('/ping', methods=['GET'])
def ping(): return pong("pong")

app.register_blueprint(api_v1, url_prefix='/api/v1')
