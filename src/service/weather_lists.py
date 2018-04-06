def getWeatherType_desc(index):
    return getWeatherType_detail(index, 'desc')

def getWeatherType_glyph(index):
    return getWeatherType_detail(index, 'glyph')

def getWeatherType_detail(index, detail):
    return weather_type[index][detail]

weather_type = {'NA': {'desc': 'Not available',
                       'glyph': 'wi-na'},
                '0': {'desc': 'Clear night',
                      'glyph': 'wi-night-clear'},
                '1': {'desc': 'Sunny day',
                      'glyph': 'wi-day-sunny'},
                '2': {'desc': 'Partly cloudy(night)',
                      'glyph': 'wi-night-alt-partly-cloudy'},
                '3': {'desc': 'Partly cloudy(day)',
                      'glyph': 'wi-day-sunny-overcast'},
                '4': {'desc': 'Not used',
                      'glyph': 'wi-na'},
                '5': {'desc': 'Mist',
                      'glyph': 'wi-dust'},
                '6': {'desc': 'Fog',
                      'glyph': 'wi-fog'},
                '7': {'desc': 'Cloudy',
                      'glyph': 'wi-cloud'},
                '8': {'desc': 'Overcast',
                      'glyph': 'wi-cloudy'},
                '9': {'desc': 'Light rain shower(night)',
                      'glyph': 'wi-night-alt-showers'},
                '10': {'desc': 'Light rain shower(day)',
                       'glyph': 'wi-day-showers'},
                '11': {'desc': 'Drizzle',
                       'glyph': 'wi-sprinkle'},
                '12': {'desc': 'Light rain',
                       'glyph': 'wi-showers'},
                '13': {'desc': 'Heavy rain shower(night)',
                       'glyph': 'wi-night-alt-rain'},
                '14': {'desc': 'Heavy rain shower(day)',
                       'glyph': 'wi-day-rain',
                       'img': 'weather_heavy-rain-day.png'},
                '15': {'desc': 'Heavy rain',
                       'glyph': 'wi-rain'},
                '16': {'desc': 'Sleet shower(night)',
                       'glyph': 'wi-night-sleet'},
                '17': {'desc': 'Sleet shower(day)',
                       'glyph': 'wi-day-sleet'},
                '18': {'desc': 'Sleet',
                       'glyph': 'wi-sleet'},
                '19': {'desc': 'Hail shower(night)',
                       'glyph': 'wi-night-hail'},
                '20': {'desc': 'Hail shower(day)',
                       'glyph': 'wi-day-hail'},
                '21': {'desc': 'Hail',
                       'glyph': 'wi-hail'},
                '22': {'desc': 'Light snow shower(night)',
                       'glyph': 'wi-night-alt-snow'},
                '23': {'desc': 'Light snow shower(day)',
                       'glyph': 'wi-day-snow'},
                '24': {'desc': 'Light snow',
                       'glyph': 'wi-snow'},
                '25': {'desc': 'Heavy snow shower(night)',
                       'glyph': 'wi-night-alt-snow'},
                '26': {'desc': 'Heavy snow shower(day)',
                       'glyph': 'wi-day-snow'},
                '27': {'desc': 'Heavy snow',
                       'glyph': 'wi-snow'},
                '28': {'desc': 'Thunder shower(night)',
                       'glyph': 'wi-night-alt-lightning'},
                '29': {'desc': 'Thunder shower(day)',
                       'glyph': 'wi-day-lightning'},
                '30': {'desc': 'Thunder',
                       'glyph': 'wi-lightning'}}

def getWind_glyphDegreeFrom(direction):
    return getWind_glyph(direction, 'degree_from')

def getWind_glyphDegreeTo(direction):
    return getWind_glyph(direction, 'degree_to')

def getWind_glyphCardinalFrom(direction):
    return getWind_glyph(direction, 'cardinal_from')

def getWind_glyphCardinalTo(direction):
    return getWind_glyph(direction, 'cardinal_to')

def getWind_glyph(direction, detail):
    return wind[direction.lower()]['glyph'][detail]

wind = {'n': {'glyph': {'degree_from': 'from-0-deg',
                        'degree_to': 'towards-180-deg',
                        'cardinal_from': 'wi-from-n',
                        'cardinal_to': 'wi-towards-s',
                        'arrow': ''}},
        'nne': {'glyph': {'degree_from': 'from-23-deg',
                          'degree_to': 'towards-203-deg',
                          'cardinal_from': 'wi-from-nne',
                          'cardinal_to': 'wi-towards-ssw',
                        'arrow': ''}},
        'ne': {'glyph': {'degree_from': 'from-45-deg',
                         'degree_to': 'towards-225-deg',
                         'cardinal_from': 'wi-from-ne',
                         'cardinal_to': 'wi-towards-sw'}},
        'ene': {'glyph': {'degree_from': 'from-68-deg',
                          'degree_to': 'towards-248-deg',
                          'cardinal_from': 'wi-from-ene',
                          'cardinal_to': 'wi-towards-wsw'}},
        'e': {'glyph': {'degree_from': 'from-90-deg',
                        'degree_to': 'towards-270-deg',
                        'cardinal_from': 'wi-from-e',
                        'cardinal_to': 'wi-towards-w'}},
        'ese': {'glyph': {'degree_from': 'from-113-deg',
                          'degree_to': 'towards-293-deg',
                          'cardinal_from': 'wi-from-ese',
                          'cardinal_to': 'wi-towards-wnw'}},
        'se': {'glyph': {'degree_from': 'from-135-deg',
                         'degree_to': 'towards-313-deg',
                         'cardinal_from': 'wi-from-se',
                         'cardinal_to': 'wi-towards-nw'}},
        'sse': {'glyph': {'degree_from': 'from-158-deg',
                          'degree_to': 'towards-336-deg',
                          'cardinal_from': 'wi-from-sse',
                          'cardinal_to': 'wi-towards-nnw'}},
        's': {'glyph': {'degree_from': 'from-180-deg',
                        'degree_to': 'towards-0-deg',
                        'cardinal_from': 'wi-from-s',
                        'cardinal_to': 'wi-towards-n'}},
        'ssw': {'glyph': {'degree_from': 'from-203-deg',
                          'degree_to': 'towards-23-deg',
                          'cardinal_from': 'wi-from-ssw',
                          'cardinal_to': 'wi-towards-nne'}},
        'sw': {'glyph': {'degree_from': 'from-225-deg',
                         'degree_to': 'towards-45-deg',
                         'cardinal_from': 'wi-from-sw',
                         'cardinal_to': 'wi-towards-ne'}},
        'wsw': {'glyph': {'degree_from': 'from-248-deg',
                          'degree_to': 'towards-68-deg',
                          'cardinal_from': 'wi-from-wsw',
                          'cardinal_to': 'wi-towards-ene'}},
        'w': {'glyph': {'degree_from': 'from-270-deg',
                        'degree_to': 'towards-90-deg',
                        'cardinal_from': 'wi-from-w',
                        'cardinal_to': 'wi-towards-e'}},
        'wnw': {'glyph': {'degree_from': 'from-293-deg',
                          'degree_to': 'towards-113-deg',
                          'cardinal_from': 'wi-from-wnw',
                          'cardinal_to': 'wi-towards-ese'}},
        'nw': {'glyph': {'degree_from': 'from-313-deg',
                         'degree_to': 'towards-135-deg',
                         'cardinal_from': 'wi-from-nw',
                         'cardinal_to': 'wi-towards-se'}},
        'nnw': {'glyph': {'degree_from': 'from-336-deg',
                          'degree_to': 'towards-158-deg',
                          'cardinal_from': 'wi-from-nnw',
                          'cardinal_to': 'wi-towards-sse'}}}

def getVisibility_desc(index):
    return getVisibility_detail(index, 'desc')

def getVisibility_dist(index):
    return getVisibility_detail(index, 'dist')

def getVisibility_detail(index, detail):
    return visibility[index][detail]

visibility = {'UN': {'desc': 'Unknown',
                     'dist': '-'},
              'VP': {'desc': 'Very poor',
                     'dist': 'Less than 1 km'},
              'PO': {'desc': 'Poor',
                     'dist': 'Between 1 - 4 km'},
              'MO': {'desc': 'Moderate',
                     'dist': 'Between 4 - 10 km'},
              'GO': {'desc': 'Good',
                     'dist': 'Between 10 - 20 km'},
              'VG': {'desc': 'Very good',
                     'dist': 'Between 20 - 40 km'},
              'EX': {'desc': 'Excellent',
                     'dist': 'More than 40 km'}}

def getUV_desc(index):
    return getUV_detail(index, 'desc')

def getUV_protection(index):
    return getUV_detail(index, 'protection')

def getUV_colour(index):
    return getUV_detail(index, 'colour')

def getUV_detail(index, detail):
    for item in uv:
        if index in item['index']:
            return item[detail]

uv = [{'index': [0],
       'desc': '-',
       'protection': '-',
       'colour': '#ffffff'},
      {'index': [1, 2],
       'desc': 'Low',
       'protection': 'No protection required.You can safely stay outside',
       'colour': '#289500'},
      {'index': [3, 4, 5],
       'desc': 'Moderate',
       'protection' : 'Seek shade during midday hours, cover up and wear sunscreen',
       'colour': '#f7e400'},
      {'index': [6, 7],
       'desc': 'High',
       'protection': 'Seek shade during midday hours, cover up and wear sunscreen',
       'colour': '#f85900'},
      {'index': [8, 9, 10],
       'desc': 'Very high',
       'protection': 'Avoid being outside during midday hours. Shirt, sunscreen and hat are essential',
       'colour': '#d8001d'},
      {'index': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
       'desc': 'Extreme',
       'protection': 'Avoid being outside during midday hours. Shirt, sunscreen and hat essential',
       'colour': '#6b49c8'}]