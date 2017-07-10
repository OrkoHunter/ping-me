# -*- coding: utf-8 -*-
"""Command line execution listener module of ping-me"""
from __future__ import print_function
from __future__ import unicode_literals
from dateutil import parser
import argparse
import datetime
import getpass
import hashlib
import os
import parsedatetime
import sys
import time

import ping_me.authenticate
import ping_me.engine

home = os.path.expanduser("~")
cal = parsedatetime.Calendar()

def main():
    """Parse the arguments using argparse package"""
    argparser = argparse.ArgumentParser(description='ping-me')

    argparser.add_argument("-e", action="store_true", default=False)
    argparser.add_argument("-V", "--version", action="store_true",
                           default=False)
    argparser.add_argument("-d", "--date", action="store", dest="DATE",
                           default=None, nargs="+")
    argparser.add_argument("-t", "--time", action="store", dest="TIME",
                           default=None, nargs="+")
    argparser.add_argument("message", action="store", help="Message",
                           default=None, nargs="*")
    argparser.add_argument("-v", action="store_true", default=False)

    args = argparser.parse_args()
    process(args)


def process(args):
    """Process the arguments. Call engine if flags are used."""
    if args.e:
        detailed_usage()
        sys.exit(2)
    if args.version:
        import release
        print(release.__version__)
        sys.exit(2)

    if args.DATE is not None and args.TIME is not None:
        message = ' '.join(args.message).lstrip('to ')
        date_time = parser.parse(' '.join(args.DATE) +
                                 ' ' + ' '.join(args.TIME))
        if len(message) == 0:
            print("What is the message of your reminder?\n")
            print("Use ping-me -h for help\n")
            sys.exit(2)
        ping_me.engine.engine(message, date_time.year, date_time.month,
                              date_time.day, date_time.hour, date_time.minute,
                              args.v)
    elif args.TIME is not None:
        m_time = parser.parse(' '.join(args.TIME))
        c_time = datetime.datetime.now()
        if (m_time - c_time).days == -1:
            m_time += datetime.timedelta(1)
        message = ' '.join(args.message).lstrip('to ')
        if len(message) == 0:
            print("What is the message of your reminder?\n")
            print("Use ping-me -h for help\n")
            sys.exit(2)
        ping_me.engine.engine(message, m_time.year, m_time.month,
                              m_time.day, m_time.hour, m_time.minute, args.v)
    elif args.DATE is not None:
        c_time = repr(time.localtime().tm_hour) + ":" + \
                 repr(time.localtime().tm_min)
        m_date = parser.parse(' '.join(args.DATE) + ' ' + c_time)
        message = ' '.join(args.message).lstrip('to ')
        if len(message) == 0:
            print("What is the message of your reminder?\n")
            print("Use ping-me -h for help\n")
            sys.exit(2)
        ping_me.engine.engine(message, m_date.year, m_date.month,
                              m_date.day, m_date.hour, m_date.minute, args.v)
    else:
        if len(args.message) == 0:
            sys.stderr.write("Use ping-me -h for help\n")
            sys.exit(2)
        elif len(args.message) == 1 and args.message == ['config']:
            ping_me.authenticate.newuser()
        elif len(args.message) == 1 and args.message == ['reconfig']:
            reconfig()
        else:
            nlp_process(args)

def nlp_process(args):
    """Process arguments using Natural Language Processing."""
    # If there is something like "to do something in 2 mins"
    try:
        mins_index = args.message.index('mins')
        args.message[mins_index] = 'minutes'
    except ValueError:
        pass
    to_parse = ' '.join(args.message)
    try:
        m_date = cal.nlp(to_parse)[0][0]
    except TypeError:
        print("Sorry, couldn't understand your message. Try again.")
        sys.exit(2)
    # Remove the keywords
    keywords = cal.nlp(to_parse)[0][-1].split()
    for word in keywords:
        args.message.remove(word)
    # Remove redundant word 'this'
    try:
        args.message.remove('this')
    except ValueError:
        pass
    if 'to' in args.message:
        args.message.remove('to')
    message = ' '.join(args.message)
    ping_me.engine.engine(message, m_date.year, m_date.month,
                          m_date.day, m_date.hour, m_date.minute,
                          args.v)


def detailed_usage():
    """Detailed documentation of ping-me."""
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
    print(f + s*11 + d*4 + f + s*11 + b + f + s + f + (r*5)[1:] + f + s*2 +
          f + s*15 + p + s + f + (r*4)[1:])
    print("")
    print("ping-me works well with time and date flags already. " +
          "Use 'ping-me -h' for that option. " +
          "However, ping-me is smart enough to work without flags.\n")
    print("Examples : ")
    print("\t\t1. ping-me to call mom tonight")
    print("\t\t2. ping-me to buy milk early today")
    print("\t\t3. ping-me to go home seven days from now")
    print("\t\t4. ping-me to take a nap this afternoon")
    print("\t\t5. ping-me to go workout next month")
    print("")
    print("Report (and track process on fixing) bugs on " +
          "https://github.com/OrkoHunter/ping-me. Or simply write a mail " +
          "to Himanshu Mishra at himanshumishra[at]iitkgp[dot]ac[dot]in")


def reconfig():
    """Reconfigure the user. Removes all the information of existing one."""
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
