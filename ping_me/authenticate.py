"""The authentication module of ping-me"""

import csv
import getpass
import hashlib
import os
import re
import sys

import phonenumbers
import ping_me
from ping_me.data import module_locator

home = os.path.expanduser("~")


def extract_email():
    f = open(home + '/.pingmeconfig', 'r')
    email = ""
    next_one = False  # If true then the next line contains our result
    for line in f.readlines():
        if next_one == True:
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
        if next_one == True:
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
        if next_one == True:
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
        if next_one == True:
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
    repass = hashlib.md5(getpass.getpass("Re-enter : ").rstrip()).hexdigest()
    while(password != repass):
        sys.stderr.write("Password match failed. Try again.\n")
        password = hashlib.md5(getpass.getpass().rstrip()).hexdigest()
        repass = hashlib.md5(getpass.getpass("Re-enter : " +
                                             "").rstrip()).hexdigest()

    code_to_country = {}
    # Location of the csv file is ambiguous
    csv_path = module_locator.modeule_path()
    csvfile = open(csv_path + "/countrylist.csv")
    reader = csv.DictReader(csvfile)
    for row in reader:
        code_to_country[row["ITU-T Telephone Code"]] = row["Common Name"]

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
    countery_name = code_to_country['+' + country_code]

    save_password = 'NO'
    sys.stdout.write("Prompt for password ? (Y/n) : ")
    opt = sys.stdin.read(1)
    if opt == 'n':
        save_password = 'YES'

    config_file = open(home + '/.pingmeconfig', 'w+')
    config_file.write('[email]\n\t' + email + '\n')
    config_file.write('[password]\n\t' + password + '\n')
    config_file.write('[phone]\n\t' + country_code + ' ' + number + ' ' +
                      countery_name + '\n')
    config_file.write("[preference]\n\t" + "SAVE_PASSWORD = " + save_password\
                      + "\n")
    config_file.close()


def olduser():
    password = hashlib.md5(getpass.getpass().rstrip()).hexdigest()
    if password == ping_me.authenticate.extract_password():
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
