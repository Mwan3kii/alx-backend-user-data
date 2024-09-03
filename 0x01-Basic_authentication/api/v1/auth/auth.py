#!/usr/bin/env python3
"""Class to manage the API authentication.
"""
import re
from typing import List, TypeVar
from flask import request
from fnmatch import fnmatch


class Auth:
    """Manage Api authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns True if path is not in list str exclude_paths"""
        if path is None or excluded_paths is None:
            return True
        for excluded_path in excluded_paths:
            if fnmatch(path, excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return value of header request else none"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None for now."""
        return None
