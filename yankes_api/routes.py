from . import app
from .domain.faskes import get_hospital_by_prov, get_isolations, get_okupansis, get_provinces
from flask import jsonify
from .utils import make_api_response

@app.route('/')
def index():
    return jsonify({
            'message': 'API for realtime bed monitoring',
            'paths': { 
                '/province': 'retrieve province',
                '/hospitals/<int:id>': 'retrieve hospitals in a province. use id from /province',
                '/occupation/<int:id>': 'retrieve occupations for every hospitals in a province. use id from /province',
                '/isolations': 'retrieve isolation rooms'
            }
        })


@app.route('/province',  methods=['GET'])
def api_get_provinces():
    return make_api_response(get_provinces())

@app.route('/hospitals/<int:idprov>',  methods=['GET'])
def api_get_hospital(idprov):
    return make_api_response(get_hospital_by_prov(idprov))

@app.route('/occupation/<int:idprov>',  methods=['GET'])
def okupansi(idprov):
    return make_api_response(get_okupansis(idprov))

@app.route('/isolations', methods=['GET'])
def isolations():
    return make_api_response(get_isolations())