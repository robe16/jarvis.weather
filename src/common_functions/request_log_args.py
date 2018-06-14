from resources.global_resources.variables import service_header_clientid_label
from common_functions.query_to_string import convert_query_to_string


def get_request_log_args(request):
    #
    urlparts = request.urlparts
    #
    try:
        client_ip = request.headers['X-Forwarded-For']
    except:
        client_ip = request['REMOTE_ADDR']
    #
    try:
        server_ip = request.headers['X-Real-IP']
    except:
        server_ip = urlparts.hostname
    #
    try:
        client_user = request.headers[service_header_clientid_label]
    except:
        client_user = request['REMOTE_ADDR']
    #
    server_request_query = convert_query_to_string(request.query) if request.query_string else '-'
    server_request_body = request.body.read() if request.body.read() != '' else '-'
    #
    return {'client_ip': client_ip,
            'client_user': client_user,
            'server_ip': server_ip,
            'server_thread_port': urlparts.port,
            'server_method': request.method,
            'server_request_uri': urlparts.path,
            'server_request_query': server_request_query,
            'server_request_body': server_request_body}
