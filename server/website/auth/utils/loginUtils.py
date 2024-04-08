# -- encoding: utf-8 --
"""
Copyright (c) 2024 - Blipo
"""

import os
import hashlib
import binascii
import bcrypt

def hash_pass(password):
    # Convert password to bytes and hash
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed

def verify_pass(password, hashed_password):
    # Check a password against the hashed version
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)