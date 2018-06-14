from resources.global_resources.variables import service_header_clientid_label


def enable_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = service_header_clientid_label
    return response
