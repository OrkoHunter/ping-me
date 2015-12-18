#!/usr/bin/env python

"""Receive request to show notification"""
import ast
import requests
import sys
import subprocess
import time

from ping_me.utils import cryptex
import ping_me.authenticate

def main():
    while(True):
        target = "http://ping-me.himanshumishra.in/ping/"
        email = ping_me.authenticate.extract_email()
        key = ping_me.authenticate.extract_password()
        data_t = {
            "email" : email,
            "password" : key
        }
        try:
            r = requests.post(target, data=data_t)
            if ast.literal_eval(r.text)["success"] == "True":
                message = cryptex.decryptor(key, ast.literal_eval(r.text)["message"])
                # Recieved the ping 5 seconds earlier
                time.sleep(5)
                if sys.platform == 'linux2':
                    subprocess.call(['notify-send', message])
                elif sys.platform == 'darwin':
                    # Need to install `terminal-notifier`
                    # $ brew install terminal-notifier
                    subprocess.call(['terminal-notifier', '-title',
                                     'ping-me', message])
                elif sys.platform in ['win32', 'win64']:
                    # Do things for windows
                    pass
            else:
                time.sleep(1)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
