#-*-coding:utf-8-*-

import hashlib

def md5(text):
    text = to_bytes(text)
    return hashlib.md5(text).hexdigest()