#!/usr/bin/env python

"""
加解密功能
"""

import base64


def pass_encode(user, pwd, split='の'):
    """
    :param user(str): user
    :param pwd(str): password
    :return: key(str)
    """
    string = f'{user}{split}{pwd}'.encode('utf8')
    key = base64.encodebytes(string)
    return key.decode('utf8').strip()

def pass_decode(key, split='の'):
    """
    :param key(str): 
    :return: user(str), pwd(str)
    """

    key = key.encode('utf8')
    string = base64.decodebytes(key)
    string = string.decode('utf8')
    user, pwd = string.split(split)
    return user, pwd

if __name__ == '__main__':

    user = 'walker'
    pwd = 'P@ssw0rd'

    key = pass_encode(user, pwd)
    print(key)
    user, pwd = pass_decode(key)
    print(user, pwd)
