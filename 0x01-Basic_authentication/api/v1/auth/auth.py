#!/usr/bin/env python3
"""Class to manage the API authentication.
"""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Manage Api authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns True if path is not in list str exclude_paths"""
        if path is None:
            return True
        if not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns None for now."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None for now."""
        return None
