#!/usr/bin/env python3
"""Regexing with function filter_datum"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    return re.sub(
        f"({'|'.join(map(re.escape, fields))})=[^{separator}]*",
        lambda m: f"{m.group(1)}={redaction}",
        message
    )
