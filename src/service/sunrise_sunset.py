import requests
import datetime

from common_functions.time_functions import convertISOdateResponse
from log.log import log_outbound, log_internal
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.lang.enGB.logs import *


class SunsetSunrise():

    STRsunrisesunset_BASEurl = 'api.sunrise-sunset.org/json'
    STRsunrisesunset_QUERYstring = 'lat={lat}&lng={lng}&date={date}&formatted=0'

    def __init__(self):
        pass

    #

    def get_sunrise_sunset(self, latitude, longitude, date):
        #
        jsonSunRiseSet = {}
        #
        jsonResponse = self._sunrisesunset_request(latitude, longitude, date)
        #
        if jsonResponse['status'] == 'OK':
            sunrise = convertISOdateResponse(jsonResponse['results']['sunrise'])
            sunset = convertISOdateResponse(jsonResponse['results']['sunset'])
            #
            # Following code commented as updates to Jenkinsfile should now start container with local timezone
            # if check_is_bst():
            #     sunrise += datetime.timedelta(hours=1)
            #     sunset += datetime.timedelta(hours=1)
            #
            jsonSunRiseSet = {'sunrise': sunrise.isoformat(' '),
                              'sunset': sunset.isoformat(' ')}
        #
        return jsonSunRiseSet

    # General request code

    def _sunrisesunset_request(self, lat, long, date):
        #
        url = self.STRsunrisesunset_BASEurl
        #
        query = self.STRsunrisesunset_QUERYstring.format(lat=lat, lng=long, date=date)
        #
        request_url = 'https://{url}{uri}?{query}'.format(url=url,
                                                         uri='',
                                                         query=query)
        #
        r = requests.get(request_url)
        #
        result = logPass if r.status_code == requests.codes.ok else logFail
        #
        log_outbound(result,
                     url, '', 'GET', '', query, '-',
                     r.status_code)
        #
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            return {'status': 'FAIL'}