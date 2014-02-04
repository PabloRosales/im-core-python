
from datetime import datetime

default_datetime_format = '%Y-%m-%d %H:%M:%S'
default_date_format = '%Y-%m-%d'

def str_to_datetime(date):
    return datetime.strptime(date, default_datetime_format)

def str_to_date(date):
    return datetime.strptime(date, default_date_format)

