from flask import request, jsonify
from app import app
from .models import *
from .const import HttpStatus
from .service_manager import ServiceManager


@app.route('/ProcessPayment', methods=['POST', 'GET'])
def ProcessPayment():
    if request.method == "GET":
        construct = {
            'error': ['Method Not Allowed'],
            'success': False,
        }
        response = jsonify(construct)
        response.status_code = HttpStatus.METHOD_NOT_ALLOWED
        return response
    else:
        res = ServiceManager().process_payment(request)

        return res
