# -*- coding: utf-8 -*-
"""Command line execution listener module of ping-me"""
from __future__ import print_function
from dateutil import parser
import argparse
import calendar
import datetime
import getpass
import hashlib
import os
import sys

import ping_me

home = os.path.expanduser("~")

def main():
    argparser = argparse.ArgumentParser(description='ping-me')

    argparser.add_argument("-d", "--date", action="store", dest="DATE",
                           default=None, nargs="+")
    argparser.add_argument("-t", "--time", action="store", dest="TIME",
                           default=None, nargs="+")
    argparser.add_argument("message", action="store", help="Message",
                           nargs="+")

    args = argparser.parse_args()

    message = ' '.join(args.message).lstrip('to ')
    date_time = parser.parse(' '.join(args.DATE) + ' '.join(args.TIME))

    ping_me.engine.engine(message, date_time.year, date_time.month,
                          date_time.day, date_time.hour, date_time.minute)

    '''
    try:
        optlist, message = getopt.getopt(sys.argv[1:], 'd:t:he')
    except Exception as e:
        if str(e).split()[1] == '-d' or str(e).split()[1] == '-t':
            print("Expected input after: " + str(e).split()[1])
        else:
            print("Unknown option: " + str(e).split()[1])
        usage()
        sys.exit(2)

    day = month = year = 'none'
    hour = minute = 0

    if optlist != []:
    # Proper time and date are given using -d and -t flags
        for opt, arg in optlist:
            # Processing date
            if opt == '-h':
                usage()
                sys.exit(2)
            if opt == '-e':
                detailed_usage()
                sys.exit(2)
            elif opt == '-d':
                for i in arg.split('-'):  # e.g. November-25-2015
                    try:
                    # Day and year would be integer convertible
                        if len(str(int(i))) == 4:
                            year = int(i)
                        elif len(str(int(i))) == 2 or len(str(int(i))) == 1:
                            day = int(i)
                    except ValueError:
                        # Month would be just a string
                        month = i
            # Processing time
            elif opt == '-t':
                try:
                    hour = int(arg.split(':')[0])
                    minute = int(arg.split(':')[1])
                except:
                    print("Unknown format for time: " ''.join(arg.split(':')))
                    usage()
                    sys.exit(2)

            else:
                sys.exit(2)

        if month != 'none':
            try:
                month = month_key[month[:3].title()]
            except:
                print("Unknown format for date: " + month)
                usage()
                sys.exit(2)

        ping_me.engine.engine(message, year=year, month=month,
                       day=day, hour=hour, minute=minute)
    else:
        # Nothing is given, just a plain string.
        if message == []:
            usage()
        elif message == ["config"] or message == ["reconfig"]:
            reconfig()
        else:
            # ~~print("pint-me ain't that smart now. Use the flags instead.")~~
            # time to be smart

            """
            Some time standard declarations (Totally personal, I understand)
            """
            _morning = 8
            _early_morning = 7
            _noon = 12
            _after_noon = 13
            _evening = 18
            _night = 20
            _late_night = 22

            today = datetime.date.today()

            # Day declarations
            if 'tomorrow' in message:
                day = today.day + 1
                message.remove('tomorrow')
            # x days from today
            elif 'days' in message and \
                    'from' in message and \
                    ('now' in message or 'today' in message):
                try:
                    _days_delta = int(message[message.index('days') - 1])
                    day = (today + datetime.timedelta(days=_days_delta)).day
                except:
                    try:
                        days = message[message.index('days') - 1]
                        days = text2num.text2num(days)
                        day = (today + datetime.timedelta(days=days)).day
                        month = (today + datetime.timedelta(days=days)).month
                        year = (today + datetime.timedelta(days=days)).year
                    except:
                        print("ERROR : How many days again?")
                        sys.exit(2)
                finally:
                    # There's this trick to avoid removing good keywords from
                    # the to-do message
                    try:
                        today_index = message.index('now')
                    except ValueError:
                        try:
                            today_index = message.index('today')
                        except ValueError:
                            print("Did you mean 'X days from now'?")
                            sys.exit(2)
                    message.remove(message[today_index])
                    message.remove(message[today_index - 1])  # Remove 'from'
                    message.remove(message[today_index - 2])  # Remove 'days'
                    message.remove(message[today_index - 3])  # Remove number
            elif 'next' in message and 'month' in message:
                day = 1
                if month != 12:
                    month = today.month + 1
                else:
                    month = 1
                    year = today.year + 1
                month_index = message.index('month')
                message.remove(message[month_index])
                message.remove(message[month_index - 1])
            elif 'this' in message and 'month' in message:
                day = 28
                month_index = message.index('month')
                message.remove(message[month_index])
                message.remove(message[month_index - 1])
            elif 'on' in message:
                # Could be a weekday, could be a date
                _on_indices = [i for i, x in enumerate(message) if x == "on"]
                for i in range(len(_on_indices)):
                    if (_is_a_weekday(message[_on_indices[i] + 1])):
                        _weekday = message[_on_indices[i] + 1]
                        _weekday = week_key[_weekday[:3]]
                        _del_weekday = _weekday - today.isoweekday()
                        _del_weekday += 7 if _del_weekday <= 0 else 0
                        _next_day = today + \
                            datetime.timedelta(days=_del_weekday)
                        day = _next_day.day
                        month = _next_day.month
                        year = _next_day.year
                        del message[_on_indices[i] + 1]
                        del message[_on_indices[i]]
                    elif (_is_a_date(message[_on_indices[i] + 1])):
                        # do whatever you have to do for a date
                        pass

            if 'early' in message and 'morning' in message:
                hour = _early_morning
                morning_index = message.index('morning')
                message.remove(message[morning_index])  # Remove 'morning'
                message.remove(message[morning_index - 1])  # Remove 'early'
            elif 'morning' in message:
                hour = _morning
                message.remove('morning')
            elif 'afternoon' in message:
                hour = _after_noon
                message.remove('afternoon')
            elif 'noon' in message:
                hour = _noon
                message.remove('noon')
            elif 'evening' in message:
                hour = _evening
                message.remove('evening')
            elif 'night' in message:
                hour = _night
                message.remove('night')
            elif 'late' in message and 'night' in message:
                hour = _late_night
                night_index = message.index('night')
                message.remove(message[night_index])  # Remove 'night'
                message.remove(message[night_index - 1])  # Remove 'late'
            elif 'tonight' in message:
                hour = _night
                message.remove('tonight')

            if 'to' in message:
                message.remove('to')
            if message[0] == 'this':
                message.pop(0)
            elif message[-1] == 'this':
                message.pop()
            ping_me.engine.engine(message, year=year, month=month,
                           day=day, hour=hour, minute=minute)
    '''


def _is_a_weekday(day):
    weekdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
                'friday', 'saturday']
    if day.lower() in weekdays:
        return True
    else:
        for i in range(len(weekdays)):
            weekdays[i] = weekdays[i][:3]
        if day.lower() in weekdays:
            return True
        else:
            return False


def _is_a_date(date):
    for i in date.split('-'):  # e.g. November-25-2015
        try:
        # Day and year would be integer convertible
            if len(str(int(i))) == 4:
                # Year detected
                pass
            elif len(str(int(i))) == 2 or len(str(int(i))) == 1:
                # Day detected
                pass
        except ValueError:
            # Month would be just a string
            if _is_weekday(date):
                return False
            else:
                pass
    return True


def usage():
    print("Usage : ping-me "
          + "[-d date] [-t time] "
          + "<command> <message>")
    print("")
    print("Commands : ")
    print("\tconfig\tConfigure or reconfigure your personal information "
          + "and preferences")
    print("\n'ping-me -h' brings up this text. Use 'ping-me -e to see detailed "
          + "usage with examples.")


def detailed_usage():
    print("Welcome to the detailed documentation of ping-me !")
    # Inspired from 'import this'
    s = " "; l = "_ "; r = " _"; f = "/"; b = "\\"; p = "|"; d = "— "
    print(s*6 + l*5 + s + l*4 + r + s*12 + l + r*5 + s*2 + r + s*8 + l +
          s*7 + l*4)
    print(s*5 + f + s*8 + f + s*5 + f + s*4 + f + s + b + s*10 + f + s + f +
          s*12 + f + s + b + s*6 + f + s + p + s*6 + f + s*7)
    print(s*4 + f + s*8 + f + s*5 + f + s*4 + f + s*3 + b + s*8 + f + s + f +
          s*12 + f + s*3 + b + s*4 + f + s*2 + p + s*5 + f + s*7)
    print(s*3 + f + r*4 + f + s*5 + f + s*4 + f + s*5 + b + s*6 + f + s + f +
          s*2 + r*4 + s*2 + f + 5*s + b + s*2 + f + s*3 + p + s*4 + f + l*4)
    print(s*2 + f + s*14 + f + s*4 + f + s*7 + b + s*4 + f + s + f + s*9 + f +
          s*2 + f + s*7 + b + f + s*4 + p + s*3 + f + s*7)
    print(s + f + s*14 + f + s*4 + f + s*9 + b + s*2 + f + s + f + s*9 + f +
          s*2 + f + s*14 + p + s*2 + f + s*7)
    print(f + s*11 + d*4 + f + s*11 + b + f + s + f + (r*5)[1:] + f + s*2 + f
          + s*15 + p + s + f + (r*4)[1:])
    print("")
    print("ping-me works well with time and date flags already. "
          + "Use 'ping-me -h' for that option. "
          + "However, ping-me is smart enough to work without flags.\n")
    print("Examples : ")
    print("\t\t1. ping-me to call mom tonight")
    print("\t\t2. ping-me to buy milk early today")
    print("\t\t3. ping-me to go home seven days from now")
    print("\t\t4. ping-me to take a nap this afternoon")
    print("\t\t5. ping-me to go workout next month")
    print("")
    print("Report (and track process on fixing) bugs on "
          + "https://github.com/OrkoHunter/ping-me. Or simply write a mail "
          + "to Himanshu Mishra at himanshumishra[at]iitkgp[dot]ac[dot]in")


def reconfig():
    if not os.path.exists(home + "/.pingmeconfig"):
        ping_me.authenticate.newuser()
    else:
        old_pass = hashlib.md5(getpass.getpass("Old Password : " +
                                               "").rstrip()).hexdigest()
        if old_pass == ping_me.authenticate.extract_password():
            ping_me.authenticate.newuser()
        else:
            print("Authentication failed.")
            sys.exit(2)

if __name__ == "__main__":

    main()
