#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password which is byte string"""
    salt = bcrypt.gensalt()
    hashed_passd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_passwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Expects arguments and returns boolean"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
