from bottle import HTTPResponse, HTTPError

from common_functions.request_enable_cors import enable_cors
from common_functions.request_log_args import get_request_log_args
from log.log import log_inbound
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.global_resources.variables import *


def get_sunrisesunset(request, _weather, _sunrisesunset, date):
    #
    # 'date' in YYYY-MM-DD format. Also accepts other date formats and even relative date formats.
    # If not present, date defaults to current date. Optional.
    #
    args = get_request_log_args(request)
    #
    try:
        #
        location = _weather.get_location()
        lat = location['latitude']
        long = location['longitude']
        #
        if date:
            data = _sunrisesunset.get_sunrise_sunset(lat, long, date)
        else:
            data = _sunrisesunset.get_sunrise_sunset(lat, long, 'today')
        #
        if not bool(data):
            status = httpStatusFailure
            args['result'] = logFail
        else:
            status = httpStatusSuccess
            args['result'] = logPass
        #
        args['http_response_code'] = status
        args['description'] = '-'
        log_inbound(**args)
        #
        response = HTTPResponse()
        response.status = status
        enable_cors(response)
        #
        if not isinstance(data, bool):
            response.body = data
        #
        return response
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
