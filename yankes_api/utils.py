from flask import jsonify

def make_api_response(data):
    return jsonify({ 'rows': data })