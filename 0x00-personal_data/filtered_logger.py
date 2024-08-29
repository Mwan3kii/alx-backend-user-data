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


import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes fields in type annotated"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incomming log records using filter_datum"""
        original = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original, self.SEPARATOR)
