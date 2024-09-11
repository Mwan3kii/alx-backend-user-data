#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from db import DB
from user import User
from bcrypt import hashpw, gensalt


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize auth class with instance"""
        self._db = DB()

    def _hash_password(password: str) -> bytes:
        """Return hashed bytes hased with bcrypt"""
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed

    def register_user(self, email: str, password: str) -> User:
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password.decode('utf-8'))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided email and password are valid."""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False
        except AttributeError:
            # Handle case where user object does not have the attribute `hashed_password`
            return False
