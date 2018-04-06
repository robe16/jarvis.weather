import datetime

def convertMinsToTime(date, mins_from_midnight):
    return datetime.datetime(date.year, date.month, date.day, 0, 0) + datetime.timedelta(minutes=mins_from_midnight)