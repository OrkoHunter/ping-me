"""The engine module of ping-me"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import datetime
import getpass
import os
import requests

from ping_me import authenticate
from ping_me.utils import cryptex

today = datetime.date.today()
home = os.path.expanduser("~")


def engine(message, year, month, day, hour=0, minute=0):
    """Sets the reminder"""
    if not os.path.exists(home + '/.pingmeconfig'):
        authenticate.newuser()
    else:
        if not authenticate.check_saved_password():
            authenticate.olduser()

    print("I have got this message :", message)
    d = datetime.datetime(year, month, day, hour, minute)

    print("I have to ping you on {:%Y-%m-%d %H:%M} hours.".format(d))
    d = d - datetime.timedelta(hours=10.5)  # Convert into NYC timezone

    extra = ' '*(16*(len(message)//16 + 1) - len(message))
    crypto_message = message + extra
    crypto_message = cryptex.encryptor(authenticate.extract_password(),
                                       crypto_message)
    target = "http://45.55.91.182:2012/message/"
    credentials = {'email' : authenticate.extract_email(),
                   'ping_datetime' : d.strftime("%Y-%m-%d %H:%M:00"),
                   'message' : crypto_message
                   }

    r = requests.post(target, data=credentials)
    print(r.status_code, r.reason)
