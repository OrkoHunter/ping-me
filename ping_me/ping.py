"""Command line execution listener module of ping-me"""
from __future__ import print_function
import calendar
import datetime
import getopt
import sys

import ping_me
from ping_me.depends import text2num

month_key = dict((v, k) for k, v in
                 enumerate(list(calendar.month_abbr)[1:], 1))


def main():
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
        ping_me.engine(message, year=year, month=month,
                       day=day, hour=hour, minute=minute)
    else:
        # Nothing is even, just a plain string.
        # $ ping-me to call mom tonight
        if message == []:
            usage()
        else:
            # print("pint-me ain't that smart now. Use the flags instead.")
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
                        day = message[message.index('days') - 1]
                        day = text2num.text2num(day)
                        day = (today + datetime.timedelta(days=day)).day
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
                            today_index = message.index('finally')
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
            if message[0]=='this':
                message.pop(0)
            elif message[-1]=='this':
                message.pop()
            ping_me.engine(message, year=year, month=month,
                           day=day, hour=hour, minute=minute)


def usage():
    print("Usage : ping-me "
          + "[-d date] [-t time] "
          + "message")
    print("")
    print("'ping-me -h' brings up this text. Use 'ping-me -e to see detailed "
          + "usage with examples.")


def detailed_usage():
    print("Welcome to the detailed documentation of ping-me !\n")
    print("ping-me works well with time and date flags already. "
          + "Use 'ping-me -h' for that option."
          + "However, ping-me is smart enough to work without flags.\n")
    print("Examples : ")
    print("\t\t1. ping-me to call mom tonight")
    print("\t\t2. ping-me to buy milk early today")
    print("\t\t3. ping-me to go home seven days from now")
    print("\t\t4. ping-me to take a nap this afternoon")
    print("\t\t5. pint-me to go workout next month")
    print("")
    print("Report (and track process on fixing) bugs on "
          + "https://github.com/OrkoHunter/ping-me. Or simply write a mail "
          + "to Himanshu Mishra at himanshumishra[at]iitkgp[dot]ac[dot]in")

if __name__ == "__main__":

    main()
