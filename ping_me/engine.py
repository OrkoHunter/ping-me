"""The engine module of ping-me"""
from __future__ import print_function
import datetime
import getpass
import os
import requests

import authenticate
import ping_me

today = datetime.date.today()
home = os.path.expanduser("~")


def engine(message, year, month, day, hour=0, minute=0):
    """Sets the reminder"""
    if year == 'none':
        year = today.year
    if month == 'none':
        month = today.month
    if day == 'none':
        day = today.day

    if not os.path.exists(home + '/.pingmeconfig'):
        ping_me.authenticate.newuser()
    else:
        if not ping_me.authenticate.check_saved_password():
            ping_me.authenticate.olduser()

    message = ' '.join(message).lower()
    print("I have got this message :", message)
    d = datetime.datetime(year, month, day, hour, minute)

    print("I have to ping you on {:%Y-%m-%d %H:%M} hours.".format(d))

    target = "http://45.55.91.182:2012/message/"
    credentials = {'email' : authenticate.extract_email(),
                   'ping_datetime' : d.strftime("%Y-%m-%d %H:%M:00"),
                   'message' : message
                   }

    r = requests.post(target, data=credentials)
    print(r.reason)
