"""The engine module of ping-me"""
from __future__ import print_function
import datetime
import getpass
import os

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

    print("I have got this message :", ' '.join(message).title())
    d = datetime.datetime(year, month, day, hour, minute)

    print("I have to ping you on {:%Y-%m-%d %H:%M} hours.".format(d))
