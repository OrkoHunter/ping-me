"""Command line execution listener module of ping-me"""
import calendar
import datetime
import getopt
import sys

import ping_me

month_key = dict((v, k) for k, v in
                 enumerate(list(calendar.month_abbr)[1:], 1))


def main():
    optlist, message = getopt.getopt(sys.argv[1:], 'd:t:')

    day = month = year = 'none'
    hour = minute = 0

    if optlist != []:
    # Proper time and date are given using -d and -t flags
        for opt, arg in optlist:
            # Processing date
            if opt == '-d':
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
                hour, minute = int(arg.split(':')[0]), int(arg.split(':')[1])
            else:
                sys.exit(1)

        if month != 'none':
            month = month_key[month[:3].title()]
        ping_me.engine(message, year=year, month=month,
                       day=day, hour=hour, minute=minute)
    else:
        # Nothing is even, just a plain string.
        # $ ping-me to call mom tonight
        print("pint-me ain't that smart now. Use the flags instead.")

if __name__ == "__main__":

    main()
