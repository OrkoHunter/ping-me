"""The engine module of ping-me"""
from __future__ import print_function
import datetime

def engine(message, year=1, month=1, day=1, hour=0, minute=0):
    print("I have got this message : ", ' '.join(message).title())
    d = datetime.date(year, month, day)
    t = datetime.time(hour, minute)

    print("I have to ping you on {0}-{1}-{2} at {3}:{4} hours.".format(d.day, d.month, d.year, t.hour, t.minute))


