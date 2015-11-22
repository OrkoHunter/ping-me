"""Command line execution listener module of ping-me"""
import calendar
import datetime
import getopt
import sys

import ping_me

month_key = dict((v, k) for k, v in
                 enumerate(list(calendar.month_abbr)[1:], 1))


def main():
    try:
        optlist, message = getopt.getopt(sys.argv[1:], 'd:t:he')
    except Exception as e:
        if str(e).split()[1] == '-d' \
        or str(e).split()[1] == '-t':
            print("Expected input after: " + str(e).split()[1])
        else:
            print("Unknown option: " + str(e).split()[1])
        usage()
        sys.exit(1)

    day = month = year = 'none'
    hour = minute = 0

    if optlist != []:
    # Proper time and date are given using -d and -t flags
        for opt, arg in optlist:
            # Processing date
            if opt == '-h':
                usage()
                sys.exit(1)
            if opt == '-e':
                detailed_usage()
                sys.exit(1)
            elif opt == '-d':
                for i in arg.split('-'):  # e.g. November-25-2015
                    try:
                    # Day and year would be integer convertible
                        if len(str(int(i))) == 4:
                            year = int(i)
                        elif len(str(int(i))) == 2 \
                        or len(str(int(i))) == 1:
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
                    print("Unknown format for time: "
                        + ''.join(arg.split(':')))
                    usage()
                    sys.exit(1)

            else:
                sys.exit(1)

        if month != 'none':
            try:
                month = month_key[month[:3].title()]
            except:
                print("Unknown format for date: " + month)
                usage()
                sys.exit(1)
        ping_me.engine(message, year=year, month=month,
                       day=day, hour=hour, minute=minute)
    else:
        # Nothing is even, just a plain string.
        # $ ping-me to call mom tonight
        if message == []:
            usage()
        else:
            print("pint-me ain't that smart now. Use the flags instead.")


def usage():
    print("Usage : ping-me "
        + "[-d date] [-t time] "
        + "message")
    print("")
    print("'ping-me -h' brings up this text. Use 'ping-me -e to see detailed "
        + "usage with examples.")


def detailed_usage():
    pass

if __name__ == "__main__":

    main()
