"""The authentication module of ping-me"""

import getpass
import hashlib
import re
import sys


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
    if password != repass:
        sys.stderr.write("Password match failed. Try again.\n")
        password = hashlib.md5(getpass.getpass().rstrip()).hexdigest()
        repass = hashlib.md5(getpass.getpass("Re-enter : " +
                             "").rstrip()).hexdigest()

    # To create a file (Better hack?)
    f = open('/home/' + getpass.getuser() + '/.pingmeconfig', 'w+')
    f.close()

    config_file = open('/home/' + getpass.getuser() + '/.pingmeconfig', 'r+')
    config_file.write('[email]\n\t' + email + '\n')
    config_file.write('[password]\n\t' + password + '\n')


def olduser():
    pass
