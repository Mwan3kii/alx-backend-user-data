#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password which is byte string"""
    salt = bcrypt.gensalt()
    hashed_passd = bcrypt.hashpw(password.encode(), salt)
    return hashed_passwd
