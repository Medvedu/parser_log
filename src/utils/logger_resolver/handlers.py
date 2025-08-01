__all__ = ["fetch_file_handler", "fetch_console_handler", "configure_root_logger"]

import logging
import sys


def fetch_file_handler(filename, encoding):
    file_handler = logging.FileHandler(filename, encoding=encoding)
    file_handler.setFormatter(logging.Formatter("%(message)s"))

    return file_handler


def fetch_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(message)s"))

    return console_handler


def configure_root_logger(handler):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
