#!/usr/bin/env python3
"""Basic authentication inherits from auth.
"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


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
            user_pwd: str) -> TypeVar('User'):
        """Returns User instance based on his email and passwd"""
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves User instance for a request"""
        auth_header = self.authorization_header(request)
        base64_auth = self.extract_base64_authorization_header(auth_header)
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        email, password = self.extract_user_credentials(decoded_auth)
        return self.user_object_from_credentials(email, password)
