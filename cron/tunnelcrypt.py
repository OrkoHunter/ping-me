"""This module crypts the message of ping"""

from __future__ import division
from string import ascii_lowercase

symbols = list('0123456789')
symbols.append(' ')
for i in ascii_lowercase:
    symbols.append(i)
symbols.extend(list(',.-_#@!()'))

def _convert_to_symbols(message):
    """
    Convert a list of characters into a list of integers using the symbols
    list.

    Parameters
    ----------
    message : list of characters
      The characters present in the message to encrypt

    Returns
    -------
    message : converted message
      A list of integers which symbolically represent characters
    """
    for i in range(len(message)):
        message[i] = symbols.index(message[i])

    return message


def encrypt(message, key):
    """
    Encrypt a message using a key of string

    Parameters
    ----------
    key : string
      The password hash of the user stored

    message : string
      Message to be encrypted

    Returns
    -------
    new_message : list of integers
      Integers obtained from `_convert_to_symbols`
    """
    message = message.lower()
    if len(key) < len(message):
        key = key*(len(message)//len(key) + 1)
    message = list(message)
    message = _convert_to_symbols(message)
    new_message = message[:]
    for i in range(len(message)):
        new_message[i] += symbols.index(key[i])

    return new_message


def decrypt(message, key):
    """
    Decrypt a message in the form of a list of integers

    Parameters
    ----------
    message : list of integers
      This is generated from the `encrypt` function
    key : string
      The key which was used in encryption

    Returns
    -------
    new_message = string
      The decrypted message
    """
    if len(key) < len(message):
        key = key*(len(message)//len(key) + 1)
    new_message = message[:]
    for i in range(len(message)):
        new_message[i] = symbols[message[i] - symbols.index(key[i])]

    return ''.join(new_message)
