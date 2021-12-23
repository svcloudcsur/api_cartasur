from flask import Blueprint, request, Response

from lib.ping import pong
from lib.v1.models import Models
from lib.v1.pagos import Pagos
from lib.v1.cuotas import Cuotas
from lib.v1.clientes import Clientes
from lib.v1.creditos import Creditos
from lib.v1.predictor import Predictor
from lib.v1.preprocess import Preprocess
from lib.v1.variables import Variables

from api.v1.http import get
from api.v1.http import post
from api.v1.http import put
from api.v1.http import upload

api_v1 = Blueprint('api_v1', __name__)

# -- PING -----------------------------------------------------------------
@api_v1.route('/ping', methods=['GET'])
def ping():
    return pong("pong v1")


# -------------------------------------------------------------------------
# -- CLIENTES -------------------------------------------------------------
# -------------------------------------------------------------------------
@api_v1.route('/clientes', methods=['GET'])
def get_clientes():
    return get(Clientes(), request)

@api_v1.route('/clientes', methods=['POST'])
def post_clientes():
    return upload(Clientes(), request)


# -------------------------------------------------------------------------
# -- CREDITOS -------------------------------------------------------------
# -------------------------------------------------------------------------
@api_v1.route('/creditos', methods=['GET'])
def get_creditos():
    return get(Creditos(), request)

@api_v1.route('/creditos', methods=['POST'])
def post_creditos():
    return upload(Creditos(), request)


# -------------------------------------------------------------------------
# -- CUOTAS ---------------------------------------------------------------
# -------------------------------------------------------------------------
@api_v1.route('/cuotas', methods=['GET'])
def get_cuotas():
    return get(Cuotas(), request)

@api_v1.route('/cuotas', methods=['POST'])
def post_cuotas():
    return upload(Cuotas(), request)


# -------------------------------------------------------------------------
# -- PAGOS ----------------------------------------------------------------
# -------------------------------------------------------------------------
@api_v1.route('/pagos', methods=['GET'])
def get_pagos():
    return get(Pagos(), request)

@api_v1.route('/pagos', methods=['POST'])
def post_pagos():
    return upload(Pagos(), request)


# -------------------------------------------------------------------------
# -- PRE PROCESSOR --------------------------------------------------------
# -------------------------------------------------------------------------
@api_v1.route('/variables', methods=['GET'])
def get_variables():
    return get(Variables(), request)

@api_v1.route('/variables', methods=['POST'])
def post_variables():
    return post(Variables(), request)

@api_v1.route('/preprocess', methods=['PUT'])
def put_pre_process():
    return put(Preprocess(), request)


# -------------------------------------------------------------------------
# -- PREDICT --------------------------------------------------------------
# -------------------------------------------------------------------------
@api_v1.route('/predict', methods=['POST'])
def post_predict():
    return post(Predictor(), request)


# -------------------------------------------------------------------------
# -- TRAIN MODEL ----------------------------------------------------------
# -------------------------------------------------------------------------
@api_v1.route('/models/train', methods=['PUT'])
def models_train():
    return put(Models(), request)
