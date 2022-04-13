from datetime import datetime


def get_date_string(a_date: datetime = None):
    if a_date is None:
        a_date = datetime.today()
    return a_date.strftime('%Y-%m-%d %H:%M')


def get_date_from_string(a_date_string: str):
    return datetime.strptime(a_date_string, '%Y-%m-%d %H:%M:%S')