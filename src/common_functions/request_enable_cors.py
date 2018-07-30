from resources.global_resources.variables import service_header_clientid_label, httpStatusSuccess
from bottle import HTTPResponse


def enable_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, {clientid}'.format(clientid=service_header_clientid_label)
    return response


def response_options():
    response = HTTPResponse()
    response.status = httpStatusSuccess
    return enable_cors(response)
