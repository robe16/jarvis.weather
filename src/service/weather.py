import requests
import datetime

from common_functions.time_functions import convertMinsToTime
from config.config import get_cfg_details_metofficeKey
from config.config import get_cfg_details_town
from service.weather_lists import *
from log.log import log_outbound, log_internal
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.lang.enGB.logs import *


class Weather():

    metoffice_session = requests.Session()

    STRmetoffice_BASEurl = 'http://datapoint.metoffice.gov.uk/public/data/'
    STRmetoffice_PATHlistsite = 'val/wxfcs/all/{datatype}/sitelist'
    STRmetoffice_PATHlistregion = 'txt/wxfcs/regionalforecast/{datatype}/sitelist'
    STRmetoffice_PATHforecastsite = 'val/wxfcs/all/{datatype}/{locationId}'

    LOCATION_id = ''
    LOCATION_town = ''
    LOCATION_elevation = ''
    LOCATION_latitude = ''
    LOCATION_longitude = ''
    LOCATION_region = ''
    LOCATION_unitaryAuthArea = ''
    REGION_id = ''

    def __init__(self):
        #
        town = get_cfg_details_town()
        self.getLocation(town)

    # Parameter functions

    def getParam_unit(self, params, name):
        for param in params:
            if param['name'] == name:
                return param['units']
        return False

    def getParam_unit_temp(self, params, name):
        unit = self.getParam_unit(params, name)
        if unit == 'C':
            return '&#8451;'
        elif unit == 'F':
            return '&#8457;;'
        else:
            return ''

    # Forecast

    def get_weather_forecast(self):
        #
        forecast_daily = self.get_weather_forecast_daily()
        forecast_3hourly = self.get_weather_forecast_3hourly()
        #
        # Assumption made that where day and night have seperate units defined,
        # these will be the same, therefore taken from day definition
        units_json = {}
        units_json['daily'] = self._unit_json(forecast_daily['SiteRep']['Wx']['Param'])
        units_json['3hourly'] = self._unit_json(forecast_3hourly['SiteRep']['Wx']['Param'])
        #
        location_json = {}
        location_json['name'] = LOCATION_town
        location_json['elevation'] = LOCATION_elevation
        location_json['latitude'] = LOCATION_latitude
        location_json['longitude'] = LOCATION_longitude
        location_json['region'] = LOCATION_region
        location_json['unitaryAuthArea'] = LOCATION_unitaryAuthArea
        #
        jsonForecast = {}
        jsonForecast['units'] = units_json
        jsonForecast['location'] = location_json
        jsonForecast['days'] = {}
        #
        dy_count = 0
        #
        for day_period in forecast_daily['SiteRep']['DV']['Location']['Period']:
            #
            date_json = {}
            #
            # date held in format '2012-11-21Z'
            dy_date = datetime.datetime.strptime(day_period['value'].replace('Z', ''), "%Y-%m-%d")
            dy_date_str = day_period['value'].replace('Z', '')
            #
            day_json = {}
            night_json = {}
            #
            for rep in day_period['Rep']:
                #
                if rep['$'] == 'Day':
                    #
                    day_json['weather_type'] = str(rep['W'])
                    day_json['wind_direction'] = rep['D']
                    day_json['wind_speed'] = rep['S']
                    day_json['visibility'] = getVisibility_desc(rep['V'])
                    day_json['temp'] = rep['Dm']
                    day_json['temp_feels'] = rep['FDm']
                    day_json['wind_gust'] = rep['Gn']
                    day_json['humidity'] = rep['Hn']
                    day_json['precipitation_prob'] = rep['PPd']
                    day_json['uv_index'] = getUV_desc(int(rep['U']))
                    #
                else:
                    #
                    night_json['weather_type'] = str(rep['W'])
                    night_json['wind_direction'] = rep['D']
                    night_json['wind_speed'] = rep['S']
                    night_json['visibility'] = getVisibility_desc(rep['V'])
                    night_json['temp'] = rep['Nm']
                    night_json['temp_feels'] = rep['FNm']
                    night_json['wind_gust'] = rep['Gm']
                    night_json['humidity'] = rep['Hm']
                    night_json['precipitation_prob'] = rep['PPn']
                    night_json['uv_index'] = '-'
                    #
                    #
            hourly_json = {}
            #
            for hour_period in forecast_3hourly['SiteRep']['DV']['Location']['Period']:
                #
                hour_date = datetime.datetime.strptime(hour_period['value'].replace('Z', ''), "%Y-%m-%d")
                hr_date_str = hour_period['value'].replace('Z', '')
                #
                if hr_date_str == dy_date_str:
                    #
                    hourly_json = {}
                    hr_count = 0
                    #
                    for rep in hour_period['Rep']:
                        #
                        hr_json_item = {}
                        hr_json_item['time'] = convertMinsToTime(hour_date, int(rep['$'])).strftime('%H:%M')
                        hr_json_item['weather_type'] = str(rep['W'])
                        hr_json_item['wind_direction'] = rep['D']
                        hr_json_item['wind_speed'] = rep['S']
                        hr_json_item['visibility'] = getVisibility_desc(rep['V'])
                        hr_json_item['temp'] = rep['T']
                        hr_json_item['temp_feels'] = rep['F']
                        hr_json_item['wind_gust'] = rep['G']
                        hr_json_item['humidity'] = rep['H']
                        hr_json_item['precipitation_prob'] = rep['Pp']
                        hr_json_item['uv_index'] = getUV_desc(int(rep['U']))
                        #
                        hourly_json[hr_count] = hr_json_item
                        #
                        hr_count += 1
                        #
            #
            date_json['date'] = dy_date_str
            date_json['daytime'] = day_json
            date_json['nighttime'] = night_json
            date_json['3hourly'] = hourly_json
            #
            jsonForecast['days'][dy_count] = date_json
            #
            dy_count += 1
        #
        return jsonForecast

    def get_weather_forecast_3hourly(self):
        return self._get_weather_forecast('3hourly')

    def get_weather_forecast_daily(self):
        return self._get_weather_forecast('daily')

    def _get_weather_forecast(self, frequency):
        # frequency = '3hourly' or 'daily'
        uri=self.STRmetoffice_PATHforecastsite.format(datatype='json', locationId=self.LOCATION_id)
        query_values = ['res={frequency}'.format(frequency=frequency)]
        #
        return self._metoffice_request(uri, query_values)

    # Locations

    def getLocation(self, town):
        locations = self.getLocations_list()
        #
        for location in locations:
            if location['name'] == town:
                global LOCATION_town
                LOCATION_town = town
                global LOCATION_id
                LOCATION_id = location['id']
                global LOCATION_elevation
                LOCATION_elevation = location['elevation']
                global LOCATION_latitude
                LOCATION_latitude = location['latitude']
                global LOCATION_longitude
                LOCATION_longitude = location['longitude']
                global LOCATION_region
                LOCATION_region = location['region']
                global LOCATION_unitaryAuthArea
                LOCATION_unitaryAuthArea = location['unitaryAuthArea']

    def getLocations_list(self):
        #
        uri = self.STRmetoffice_PATHlistsite.format(datatype='json')
        query_values = []
        #
        return self._metoffice_request(uri, query_values)

    # Regions

    def getRegion(self):
        regions = self.getRegions_list()
        #
        for region in regions:
            if region['@name'] == LOCATION_region:
                global REGION_id
                REGION_id = region['@id']

    def getRegions_list(self):
        #
        uri = self.STRmetoffice_PATHlistregion.format(datatype='json')
        query_values = []
        #
        return self._metoffice_request(uri, query_values)

    # General scripts

    def _unit_json(self, data):
        units_json = {}
        units_json['weather_type'] = self.getParam_unit(data, 'W')
        units_json['wind_direction'] = self.getParam_unit(data, 'D')
        units_json['wind_speed'] = self.getParam_unit(data, 'S')
        units_json['visibility'] = self.getParam_unit(data, 'V')
        units_json['temp'] = self.getParam_unit_temp(data, 'Dm')
        units_json['temp_feels'] = self.getParam_unit_temp(data, 'FDm')
        units_json['wind_gust'] = self.getParam_unit(data, 'Gn')
        units_json['humidity'] = self.getParam_unit(data, 'Hn')
        units_json['precipitation_prob'] = self.getParam_unit(data, 'PPd')
        units_json['uv_index'] = self.getParam_unit(data, 'U')
        #
        return units_json

    # General request code

    def _metoffice_request(self, uri, query_values):
        #
        query = 'key={api_key}'.format(api_key=get_cfg_details_metofficeKey())
        #
        if len(query_values):
            query += '&'
            query += '&'.join(query_values)
        #
        url = 'http://{url}{uri}?{query}'.format(url=self.STRmetoffice_BASEurl,
                                                 uri=uri,
                                                 query=query)
        #
        r = requests.get(url)
        #
        result = logPass if r.status_code == requests.codes.ok else logFail
        #
        log_outbound(result,
                     url, '', 'GET', uri, query, '-',
                     r.status_code)
        #
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            return False
