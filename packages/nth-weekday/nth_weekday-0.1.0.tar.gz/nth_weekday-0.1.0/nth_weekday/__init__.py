"""nth_weekday - """
import calendar
import time

__version__ = "0.1.0"
__author__ = "fx-kirin <fx.kirin@gmail.com>"
__all__: list = ["get_nth_weekday"]


def get_nth_weekday(weekday, year, month, nth):
    if isinstance(weekday, str):
        weekday = time.strptime(weekday, "%A").tm_wday
    return [
        cal[0]
        for cal in calendar.Calendar(weekday).monthdatescalendar(year, month)
        if cal[0].month == month
    ][nth]
