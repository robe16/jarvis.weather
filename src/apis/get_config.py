from bottle import HTTPResponse, HTTPError

from common_functions.request_log_args import get_request_log_args
from config.config import get_cfg_serviceid, get_cfg_name_long, get_cfg_name_short, get_cfg_groups, get_cfg_subservices
from log.log import log_inbound
from resources.global_resources.log_vars import logPass, logException
from resources.global_resources.variables import *


def get_config(request):
    #
    args = get_request_log_args(request)
    #
    try:
        #
        data = {'service_id': get_cfg_serviceid(),
                'name_long': get_cfg_name_long(),
                'name_short': get_cfg_name_short(),
                'subservices': get_cfg_subservices(),
                'groups': get_cfg_groups(),
                'ui_links': []
                }
        #
        status = httpStatusSuccess
        #
        args['result'] = logPass
        args['http_response_code'] = status
        args['description'] = '-'
        log_inbound(**args)
        #
        return HTTPResponse(body=data, status=status)
        #
    except Exception as e:
        #
        status = httpStatusServererror
        #
        args['result'] = logException
        args['http_response_code'] = status
        args['description'] = '-'
        args['exception'] = e
        log_inbound(**args)
        #
        raise HTTPError(status)
