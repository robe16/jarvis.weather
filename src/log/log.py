from datetime import datetime
import os

from config.config import get_cfg_serviceid
from resources.global_resources.variables import serviceType


logFileNameDateFormat = '%Y-%m-%d'
logTimeFormat = '%Y/%m/%d %H.%M.%S.%f'

logInbound = 'timestamp={timestamp}, ' + \
             'service_id={service_id}, service_type={service_type}, ' + \
             'category=INBOUND, ' + \
             'result={result}, ' + \
             'client_ip={client_ip}, client_user={client_user}, ' + \
             'server_ip={server_ip}, server_thread_port={server_thread_port}, ' + \
             'server_method={server_method}, server_request_uri={server_request_uri}, ' + \
             'server_request_query={server_request_query}, server_request_body={server_request_body}, ' + \
             'http_response_code={http_response_code}, ' + \
             'description={description}'

logInternal = 'timestamp={timestamp}, ' + \
              'service_id={service_id}, service_type={service_type}, ' + \
              'category=INTERNAL, ' + \
              'result={result}, ' + \
              'operation={operation}, ' + \
              'description={description}'

logOutbound = 'timestamp={timestamp}, ' + \
              'service_id={service_id}, service_type={service_type}, ' + \
              'category=OUTBOUND, ' + \
              'result={result}, ' + \
              'service_ip={service_ip}, service_port={service_port}, ' + \
              'service_method={service_method}, service_request_uri={service_request_uri}, ' + \
              'service_request_query={service_request_query}, service_request_body={service_request_body}, ' + \
              'http_response_code={http_response_code}, ' + \
              'description={description}'


def log_inbound(result, client_ip, client_user,
                server_ip, server_thread_port, server_method, server_request_uri, server_request_query, server_request_body,
                http_response_code,
                description='-',
                exception=False):
    #
    args = {'timestamp': _timestamp(),
            'service_id': get_cfg_serviceid(),
            'service_type': serviceType,
            'result': result,
            'client_ip': client_ip,
            'client_user': client_user,
            'server_ip': server_ip,
            'server_thread_port': server_thread_port,
            'server_method': server_method,
            'server_request_uri': server_request_uri,
            'server_request_query': server_request_query,
            'server_request_body': server_request_body,
            'http_response_code': http_response_code,
            'description': description}
    #
    log_msg = logInbound.format(**args)
    #
    if exception:
        log_msg += ', exception={exception}'.format(exception=exception)
    #
    _add_log_entry(log_msg)


def log_internal(result, operation, description='-', exception=False):
    #
    args = {'timestamp': _timestamp(),
            'service_id': get_cfg_serviceid(),
            'service_type': serviceType,
            'result': result,
            'operation': operation,
            'description': description}
    #
    log_msg = logInternal.format(**args)
    #
    if exception:
        log_msg += ', exception={exception}'.format(exception=exception)
    #
    _add_log_entry(log_msg)


def log_outbound(result,
                 service_ip, service_port, service_method, service_request_uri, service_request_query, service_request_body,
                 http_response_code,
                 description='-',
                 exception=False):
    #
    args = {'timestamp': _timestamp(),
            'service_id': get_cfg_serviceid(),
            'service_type': serviceType,
            'result': result,
            'service_ip': service_ip,
            'service_port': service_port,
            'service_method': service_method,
            'service_request_uri': service_request_uri,
            'service_request_query': service_request_query,
            'service_request_body': service_request_body,
            'http_response_code': http_response_code,
            'description': description}
    #
    log_msg = logOutbound.format(**args)
    #
    if exception:
        log_msg += ', exception={exception}'.format(exception=exception)
    #
    _add_log_entry(log_msg)


def _add_log_entry(log_msg):
    try:
        file_name = _get_log_filename()
        with open(os.path.join(os.path.dirname(__file__), 'logfiles', file_name), 'a') as output_file:
            output_file.write(log_msg + '\n')
            output_file.close()
    except Exception as e:
        pass


def _get_log_filename():
    return '{filename}.{date}.log'.format(filename=get_cfg_serviceid(),
                                          date=datetime.now().strftime(logFileNameDateFormat))


def _timestamp():
    return datetime.now().strftime(logTimeFormat)