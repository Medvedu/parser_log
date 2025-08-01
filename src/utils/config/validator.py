__all__ = ["validate"]

import os

ALLOWED_ENCODINGS = ["utf-8", "iso-8859-1", "koi8-r"]


def validate(config):
    if config.log_dir and not os.path.isdir(config.log_dir):
        print(f"Директория для вывода лога скрипта: '{config.log_dir}' не обнаружена.")
        raise NotADirectoryError(config.report_dir)

    if not config.encoding in ALLOWED_ENCODINGS:
        print(f"Кодировка {config.encoding} не поддерживается.")
        raise ValueError(config.encoding)
