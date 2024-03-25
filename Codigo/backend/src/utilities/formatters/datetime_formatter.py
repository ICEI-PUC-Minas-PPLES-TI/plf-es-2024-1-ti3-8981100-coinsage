import datetime


# just an example of a datetime formatter
def format_datetime(date_time: datetime.datetime) -> str:
    return date_time.strftime("%d-%m-%Y %H:%M:%S")
