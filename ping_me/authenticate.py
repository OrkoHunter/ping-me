"""The authentication module of ping-me"""

import csv
import getpass
import hashlib
import re
import sys

import phonenumbers


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
    with open("ping_me/data/countrylist.csv") as csvfile:
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


    # To create a file (Better hack?)
    f = open('/home/' + getpass.getuser() + '/.pingmeconfig', 'w+')
    f.close()

    config_file = open('/home/' + getpass.getuser() + '/.pingmeconfig', 'r+')
    config_file.write('[email]\n\t' + email + '\n')
    config_file.write('[password]\n\t' + password + '\n')
    config_file.write('[phone]\n\t' + country_code + ' ' + number + ' ' +
                      countery_name + '\n')
    config_file.close()


def olduser():
    pass
