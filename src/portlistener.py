from bottle import request, run, route, get

from config.config import get_cfg_port
from common_functions.request_enable_cors import response_options
from log.log import log_internal
from resources.global_resources.log_vars import logPass
from resources.lang.enGB.logs import *
from service.weather import Weather
from service.sunrise_sunset import SunsetSunrise

from apis.get_config import get_config
from apis.get_all import get_all
from apis.get_location import get_location
from apis.get_forecast import get_forecast
from apis.get_sunrisesunset import get_sunrisesunset


def start_bottle():

    ################################################################################################
    # Create device
    ################################################################################################

    _weather = Weather()
    _sunrisesunset = SunsetSunrise()

    log_internal(logPass, logDescDeviceObjectCreation, description='success')

    ################################################################################################
    # APIs
    ################################################################################################

    @route('/config', method=['OPTIONS'])
    @route('/weather/all', method=['OPTIONS'])
    @route('/weather/location', method=['OPTIONS'])
    @route('/weather/forecast/<option>', method=['OPTIONS'])
    @route('/weather/sunrise-sunset/<date>', method=['OPTIONS'])
    def api_cors_options():
        return response_options()

    @get('/config')
    def api_get_config():
        return get_config(request)

    @get('/weather/all')
    def api_get_all():
        return get_all(request, _weather, _sunrisesunset)

    @get('/weather/location')
    def api_get_location():
        return get_location(request, _weather)

    @get('/weather/forecast/<option>')
    def api_get_forecast(option):
        return get_forecast(request, _weather, option)

    @get('/weather/sunrise-sunset/<date>')
    def api_get_sunrisesunset(date):
        return get_sunrisesunset(request, _weather, _sunrisesunset, date)

    ################################################################################################

    host = '0.0.0.0'
    port = get_cfg_port()
    run(host=host, port=port, server='paste', debug=True)

    log_internal(logPass, logDescPortListener.format(port=port), description='started')

    ################################################################################################
