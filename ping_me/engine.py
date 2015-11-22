"""The engine module of ping-me"""
from __future__ import print_function
import datetime

today = datetime.date.today()


def engine(message, year, month, day, hour=0, minute=0):
    """Sets the reminder"""
    if year == 'none':
        year = today.year
    if month == 'none':
        month = today.month
    if day == 'none':
        day = today.day

    print("I have got this message :", ' '.join(message).title())
    d = datetime.datetime(year, month, day, hour, minute)

    print("I have to ping you on {:%Y-%m-%d %H:%M} hours.".format(d))
