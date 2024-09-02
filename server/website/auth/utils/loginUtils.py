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
    return hashed.decode('utf-8')

def verify_pass(password, hashed_password):
    # Convertir hashed_password de str a bytes antes de compararlo
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))