from datetime import datetime, timedelta

RFC3339_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
MILITARY_TIME_FORMAT = "%b-%d-%Y %H:%M:%S"


def rfc3339_to_datetime(date_string):
    return datetime.strptime(date_string, RFC3339_DATE_FORMAT)


def add_time(base_time, hours=0, minutes=0, seconds=0):
    return base_time + timedelta(hours=hours, minutes=minutes, seconds=seconds)


def format_date(date_to_format, date_format):
    return datetime.strftime(date_to_format, date_format)
    