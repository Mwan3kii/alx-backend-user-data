#!/usr/bin/env python3
"""Basic authentication inherits from auth.
"""
from api.v1.auth.auth import Auth


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
