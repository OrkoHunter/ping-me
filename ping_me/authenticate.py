"""The authentication module of ping-me"""

import ast
import datetime
import getpass
import hashlib
import os
import re
import requests
import sys

import phonenumbers
from ping_me.data import countrylist

home = os.path.expanduser("~")


def extract_email():
    f = open(home + '/.pingmeconfig', 'r')
    email = ""
    next_one = False  # If true then the next line contains our result
    for line in f.readlines():
        if next_one is True:
            email = line.lstrip().rstrip()
            break
        elif line == "[email]\n":
            next_one = True
    f.close()
    if email == "":
        sys.stderr.write("'$HOME/.pingmeconfig' file seems to be broken.")
        sys.exit(2)
    else:
        return email


def extract_password():
    f = open(home + '/.pingmeconfig', 'r')
    password = ""
    next_one = False  # If true then the next line contains our result
    for line in f.readlines():
        if next_one is True:
            password = line.lstrip().rstrip()
            break
        elif line == "[password]\n":
            next_one = True
    f.close()
    if password == "":
        sys.stderr.write("'$HOME/.pingmeconfig' file seems to be broken.")
        sys.exit(2)
    else:
        return password


def extract_phone():
    f = open(home + '/.pingmeconfig', 'r')
    phone = ""
    next_one = False  # If true then the next line contains our result
    for line in f.readlines():
        if next_one is True:
            phone = line.split()
            break
        elif line == "[phone]\n":
            next_one = True
    f.close()
    if phone == "":
        sys.stderr.write("'$HOME/.pingmeconfig' file seems to be broken.")
        sys.exit(2)
    else:
        return tuple(phone)  # A tuple of country code, phone number and name


def check_saved_password():
    f = open(home + '/.pingmeconfig', 'r')
    next_one = False
    for line in f.readlines():
        if next_one is True:
            return True if "YES" in line.split() else False
        if line == "[preference]\n":
            next_one = True


def newuser():
    EMAIL_REGEX = re.compile(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")

    sys.stdout.write("Email : ")
    email = sys.stdin.readline()
    while(not EMAIL_REGEX.match(email)):
        sys.stderr.write("Wrong email address. Try again.\n")
        sys.stdout.write("Email : ")
        email = sys.stdin.readline()
    email = email.rstrip()  # Remove newline character

    password = hashlib.md5(getpass.getpass().rstrip()).hexdigest()
    while(password=="d41d8cd98f00b204e9800998ecf8427e"):  # NULL
        sys.stderr.write("Invalid password. Try Again.\n")
        password = hashlib.md5(getpass.getpass().rstrip()).hexdigest()
    repass = hashlib.md5(getpass.getpass("Re-enter : ").rstrip()).hexdigest()
    while(password != repass):
        sys.stderr.write("Password match failed. Try again.\n")
        password = hashlib.md5(getpass.getpass().rstrip()).hexdigest()
        repass = hashlib.md5(getpass.getpass("Re-enter : " +
                                             "").rstrip()).hexdigest()

    while(True):
        try:
            sys.stdout.write("Phone number : ")
            read_number = sys.stdin.readline()
            read_number = phonenumbers.parse(read_number, "IN")
            while(not phonenumbers.is_valid_number(read_number)):
                sys.stderr.write("Phone number is invalid. Try again.\n")
                sys.stdout.write("Phone number : ")
                read_number = sys.stdin.readline()
                read_number = phonenumbers.parse(read_number, "IN")
            break
        except Exception as e:
            print(e)

    number = str(read_number.national_number).rstrip()
    country_code = str(read_number.country_code)
    country_name = countrylist.code_to_country['+' + country_code]

    save_password = 'YES'
    sys.stdout.write("Prompt for password ? (y/N) : ")
    opt = sys.stdin.readline()
    if opt.strip() == 'y': # New line character
        save_password = 'NO'

    target = "http://ping-me.himanshumishra.in/config/"
    credentials = {'email' : email,
                   'password' : password,
                   'phone' : number,
                   'join_date' : datetime.date.today(),
                   'os' : sys.platform,
                   'country_code' : country_code,
                   'country_name' : country_name,
                   'phone_os' : "Unknown"
                   }

    r = requests.post(target, data=credentials)

    if r.reason == "OK":
        if ast.literal_eval(r.text)["success"]=="True":
            config_file = open(home + '/.pingmeconfig', 'w+')
            config_file.write('[email]\n\t' + email + '\n')
            config_file.write('[password]\n\t' + password + '\n')
            config_file.write('[phone]\n\t' + country_code + ' ' + number +
                              ' ' + country_name + '\n')
            config_file.write("[preference]\n\t" + "SAVE_PASSWORD = " \
                              + save_password + "\n")
            config_file.close()
        else:
            sys.stderr.write("\nERROR : " + ast.literal_eval(r.text)["reason"] + "\n")
    else:
        sys.stderr.write("\nERROR : Problem on the server. Contact sysadmin\n")


def olduser():
    password = hashlib.md5(getpass.getpass().rstrip()).hexdigest()
    if password == extract_password():
        sys.stdout.write("Do you want to save this password? (y/N) : ")
        opt = sys.stdin.read(1)
        if opt == 'y':
            f = open(home + '/.pingmeconfig', 'r')
            oldlines = f.readlines()
            f.close()
            f = open(home + '/.pingmeconfig', 'w')
            for line in oldlines:
                if line == "\tSAVE_PASSWORD = NO\n":
                    f.write("\tSAVE_PASSWORD = YES\n")
                else:
                    f.write(line)
            f.close()
    else:
        sys.stderr.write("Authentication failed.\n")
        sys.exit(2)
