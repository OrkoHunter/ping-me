"""Command line execution listener module of ping-me"""
import calendar
import datetime
import getopt
import sys

import ping_me

month_key = dict((v,k) for k,v in enumerate(list(calendar.month_abbr)[1:], 1))

def main():
    optlist, message = getopt.getopt(sys.argv[1:], 'd:t:')

    day = 0
    month = ''
    year = 0
    hour = 0
    minute = 0

    for opt, arg in optlist:
        if opt=='-d':
            for i in arg.split('-'):
                try:
                    if len(str(int(i)))==4:
                        year = int(i)
                    elif len(str(int(i)))==2 or len(str(int(i)))==1:
                        day = int(i)
                except ValueError:
                    month = i
        elif opt=='-t':
            hour, minute = int(arg.split(':')[0]), int(arg.split(':')[1])
        else:
            sys.exit(1)

    ping_me.engine(message, year=year, month=month_key[month[:3].title()],
        day=day, hour=hour, minute=minute)

if __name__ == "__main__":

    main()
