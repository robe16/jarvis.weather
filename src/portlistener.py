import threading

from bottle import HTTPError
from bottle import get
from bottle import request, run, HTTPResponse
import datetime

from common_functions.query_to_string import convert_query_to_string
from config.config import get_cfg_port_listener
from config.config import get_cfg_serviceid, get_cfg_name_long, get_cfg_name_short, get_cfg_groups, get_cfg_subservices
from log.log import log_inbound, log_internal, log_outbound
from resources.global_resources.exposed_apis import *
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.global_resources.variables import *
from resources.lang.enGB.logs import *
from service.weather import Weather
from service.sunrise_sunset import SunsetSunrise


def start_bottle(port_threads):

    ################################################################################################
    # Create device
    ################################################################################################

    _weather = Weather()
    _sunrisesunset = SunsetSunrise()

    log_internal(logPass, logDescDeviceObjectCreation, description='success')

    ################################################################################################
    # Enable cross domain scripting
    ################################################################################################

    def enable_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        return response

    ################################################################################################
    # Log arguments
    ################################################################################################

    def _get_log_args(request):
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
        server_request_body = request.body.read() if request.body.read()!='' else '-'
        #
        return {'client_ip': client_ip,
                'client_user': client_user,
                'server_ip': server_ip,
                'server_thread_port': urlparts.port,
                'server_method': request.method,
                'server_request_uri': urlparts.path,
                'server_request_query': server_request_query,
                'server_request_body': server_request_body}

    ################################################################################################
    # Service info & Groups
    ################################################################################################

    @get(uri_config)
    def get_config():
        #
        args = _get_log_args(request)
        #
        try:
            #
            data = {'service_id': get_cfg_serviceid(),
                    'name_long': get_cfg_name_long(),
                    'name_short': get_cfg_name_short(),
                    'subservices': get_cfg_subservices(),
                    'groups': get_cfg_groups()}
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

    ################################################################################################
    # Location
    ################################################################################################

    @get(uri_get_location)
    def get_headlines(option):
        #
        args = _get_log_args(request)
        #
        try:
            #
            data = _weather.get_location()
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
            if isinstance(data, bool):
                return HTTPResponse(status=status)
            else:
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

    ################################################################################################
    # Forecast
    ################################################################################################

    @get(uri_get_weather_forecast)
    def get_headlines(option):
        #
        args = _get_log_args(request)
        #
        try:
            #
            if option == 'all':
                data = _weather.get_weather_forecast()
            elif option == '3hourly':
                data = False
            elif option == 'daily':
                data = False
            else:
                data = False
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
            if isinstance(data, bool):
                return HTTPResponse(status=status)
            else:
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

    ################################################################################################
    # Sunrise/Sunset
    ################################################################################################

    @get(uri_get_weather_sunriseset)
    def get_headlines(date):
        #
        # 'date' in YYYY-MM-DD format. Also accepts other date formats and even relative date formats.
        # If not present, date defaults to current date. Optional.
        #
        args = _get_log_args(request)
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
                data = False
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
            if isinstance(data, bool):
                return HTTPResponse(status=status)
            else:
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

    ################################################################################################

    def bottle_run(x_host, x_port):
        log_internal(logPass, logDescPortListener.format(port=x_port), description='started')
        run(host=x_host, port=x_port, debug=True)

    ################################################################################################

    host = 'localhost'
    ports = get_cfg_port_listener()
    for port in ports:
        t = threading.Thread(target=bottle_run, args=(host, port,))
        port_threads.append(t)

    # Start all threads
    for t in port_threads:
        t.start()
    # Use .join() for all threads to keep main process 'alive'
    for t in port_threads:
        t.join()
