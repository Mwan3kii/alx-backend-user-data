#!/usr/bin/env python3
"""Class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar
import request from flask


class Auth:
    """Manage Api authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False for now."""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns None for now."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None for now."""
        return None
