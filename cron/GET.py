#!/usr/bin/env python

import urllib2
import ping_me
import hashlib
import sys
import subprocess
from ping_me.utils import cryptex


country = ping_me.authenticate.extract_phone()[2]
filename = country[:2] + country[-2:]
del country
target = "http://www.himanshumishra.in/pingme/cron/" + filename + '.txt'
email = ping_me.authenticate.extract_email()
password = ping_me.authenticate.extract_password()
hashed_email = hashlib.md5(email).hexdigest()
del email
data = urllib2.urlopen(target)

found = False
for line in data:
    line = line.split()
    if line[0] == hashed_email:
        found = True
        for i in range(1, len(line)):
            line[i] = int(line[i])
        message = cryptex.decryptor(password, line[1:])
        if sys.platform == 'linux2':
            subprocess.call(['notify-send', message])
        elif sys.platform == 'darwin':
            subprocess.call(['terminal-notifier', '-title', 'ping-me', 'Ping!'])
        elif sys.platform in ['win32', 'win64']:
            # Do things for windows
            pass

# If not found in the country's name, search in XXXX.txt
if not found:
    target = 'http://www.himanshumishra.in/pingme/cron/XXXX.txt'
    data = urllib2.urlopen(target)
    for line in data:
        line = line.split()
        if line[0] == hashed_email:
            found = True
            for i in range(1, len(line)):
                line[i] = int(line[i])
            message = cryptex.decryptor(password, line[1:])
            if sys.platform == 'linux2':
                subprocess.call(['notify-send', message])
            elif sys.platform == 'darwin':
                subprocess.call(['terminal-notifier', '-title', message])
            elif sys.platform in ['win32', 'win64']:
                # Do things for windows
                pass


del target
del data
del hashed_email
