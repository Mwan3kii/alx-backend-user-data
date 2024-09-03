#!/usr/bin/env python3
"""Basic authentication inherits from auth.
"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User

UserType = TypeVar('User', bound=User)


class BasicAuth(Auth):
    """Basic authentication"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Returns base64 of authorizzation header"""
        auth_header = isinstance(authorization_header, str)
        if authorization_header is None or not auth_header:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Returns decoded value Base64 string"""
        base_header = isinstance(base64_authorization_header, str)
        if base64_authorization_header is None or not base_header:
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """Returns user email and passwd from base64 decoded value"""
        base64_auth = isinstance(decoded_base64_authorization_header, str)
        if decoded_base64_authorization_header is None or not base64_auth:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> UserType:
        """Returns User instance based on his email and passwd"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user = User.search(user_email)
        if not user:
            return None
        user = user[0]
        if user.is_valid_password(user_pwd):
            return user
        return None
