"""The engine module of ping-me"""
from __future__ import print_function
import datetime
import getpass
import os
import requests

from ping_me import authenticate
from ping_me import cryptex

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
        authenticate.newuser()
    else:
        if not authenticate.check_saved_password():
            authenticate.olduser()

    message = ' '.join(message).lower()
    print("I have got this message :", message)
    d = datetime.datetime(year, month, day, hour, minute)

    print("I have to ping you on {:%Y-%m-%d %H:%M} hours.".format(d))

    extra = (len(message) - len(message)%16)*' '
    crypto_message = message + extra
    cryptex.encryptor(authenticate.extract_password(), crypto_message)
    target = "http://45.55.91.182:2012/message/"
    credentials = {'email' : authenticate.extract_email(),
                   'ping_datetime' : d.strftime("%Y-%m-%d %H:%M:00"),
                   'message' : crypto_message
                   }

    r = requests.post(target, data=credentials)
    print(r.reason)
