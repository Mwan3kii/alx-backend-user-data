#!/usr/bin/env python3
"""Regexing with function filter_datum"""
import re
from typing import List
import logging
import mysql.connector
from mysql.connector import connection
import os

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    return re.sub(
        f"({'|'.join(map(re.escape, fields))})=[^{separator}]*",
        lambda m: f"{m.group(1)}={redaction}",
        message
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
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
        return filter_datum(self.fields, self.REDACTION,
                            original, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Takes no arguments and return object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """Returns connector to database using credentials"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=passwd,
        host=host,
        database=db_name
    )


def main() -> None:
    """Obtains database connection and retrieve rows in users table"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor:
        row_dict = dict(zip([desc[0] for desc in cursor.description], row))
        message = "; ".join([f"{key}={value}" for key, value in row_dict.items()])
        logger.info(message)
    
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
