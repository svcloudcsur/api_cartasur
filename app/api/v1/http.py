# -------------------------------------------------------------------------
#  This class implements all the HTTP verbs used
# -------------------------------------------------------------------------
import sys
import traceback
from flask import jsonify
from datetime import datetime

# -------------------------------------------------------------------------
#  GET
# -------------------------------------------------------------------------
def get(klass, request):
    try:
        return jsonify(klass.get())
    except:
        return jsonify("ERROR: {}. Quizas no implementa GET?".format(klass.__class__.__name__)), 500


# -------------------------------------------------------------------------
#  PUT
# -------------------------------------------------------------------------
def put(klass, request):
    try:
        return jsonify(klass.put(request))
    except:
        return jsonify("ERROR: {}. Quizas no implementa PUT?".format(klass.__class__.__name__)), 500


# -------------------------------------------------------------------------
#  POST
# -------------------------------------------------------------------------
def post(klass, request):
    try:
        return jsonify({'response' : klass.post(request)})
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return jsonify("ERROR: llamando a {}".format(klass.__class__.__name__)), 500


# -------------------------------------------------------------------------
#  UPLOAD
# -------------------------------------------------------------------------
def upload(klass, request):
    try:
        if(klass.update(request.files['file'])):
            return jsonify("{} fue cargada correctamente! [Fecha: {}]".format(klass.__class__.__name__, datetime.now())), 200
        else:
            return jsonify("ERROR cargando {} en la base de datos".format(klass.__class__.__name__)), 500
    except:
        return jsonify("ERROR en {} subiendo el file!".format(klass.__class__.__name__)), 500
