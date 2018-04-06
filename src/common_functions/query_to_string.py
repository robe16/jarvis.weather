def convert_query_to_string(bottleDict):
    #
    str = '{'
    for k in bottleDict:
        str += ', ' if not str == '{' else ''
        str += '"{key}":"{value}"'.format(key=k, value=bottleDict[k])
    str += '}'
    #
    return str
