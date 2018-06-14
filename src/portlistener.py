import threading

from bottle import get
from bottle import request, run

from config.config import get_cfg_port_listener
from log.log import log_internal
from resources.global_resources.log_vars import logPass
from resources.lang.enGB.logs import *
from service.weather import Weather
from service.sunrise_sunset import SunsetSunrise

from apis.uri_config import get_config
from apis.uri_get_all import get_all
from apis.uri_get_location import get_location
from apis.uri_get_forecast import get_forecast
from apis.uri_get_sunrisesunset import get_sunrisesunset


def start_bottle(port_threads):

    ################################################################################################
    # Create device
    ################################################################################################

    _weather = Weather()
    _sunrisesunset = SunsetSunrise()

    log_internal(logPass, logDescDeviceObjectCreation, description='success')

    ################################################################################################
    # APIs
    ################################################################################################

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
