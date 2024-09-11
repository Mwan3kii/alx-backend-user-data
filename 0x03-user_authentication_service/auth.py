#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Return hashed bytes hased with bcrypt"""
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed
