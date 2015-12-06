#!/usr/bin/env python

"""Receive request to show notification"""
import urllib2
import hashlib
import sys
import subprocess
import time

from ping_me.utils import cryptex
import ping_me

while(True):
    # The try/except is for the case when the file might not exist
    try:
        country = ping_me.authenticate.extract_phone()[2]
        filename = country[:2] + country[-2:] + '.txt'
        target = "http://www.himanshumishra.in/pingme/cron/" + filename
        email = ping_me.authenticate.extract_email()
        hashed_email = hashlib.md5(email).hexdigest()
        key = ping_me.authenticate.extract_password()

        data = urllib2.urlopen(target)

        for line in data:
            line = line.split()
            if line[0] == hashed_email:
                # ping time!
                message = cryptex.decryptor(key, line[1])
                if sys.platform == 'linux2':
                    subprocess.call(['notify-send', message])
                elif sys.platform == 'darwin':
                    subprocess.call(['terminal-notifier', '-title', 'ping-me',
                                     message])
                elif sys.platform in ['win32', 'win64']:
                    # Do things for windows
                    pass

        # If not found in the country's name, search in XXXX.txt
        if not found:
            target = 'http://www.himanshumishra.in/pingme/cron/XXXX.txt'
            data = urllib.urlopen(target)
            for line in data:
                line = line.split()
                if line[0] == hashed_email:
                    found = True
                    message = cryptex.decryptor(key, line[1])
                    if sys.platform == 'linux2':
                        subprocess.call(['notify-send', message])
                    elif sys.platform == 'darwin':
                        subprocess.call(['terminal-notifier', '-title', message])
                    elif sys.platform in ['win32', 'win64']:
                        # Do things for windows
                        pass
        time.sleep(4)
    except:
        time.sleep(4)
