__all__ = ["fetch_log_entity"]

import os
import re
from collections import namedtuple
from datetime import datetime
from os import listdir
from os.path import isfile

SEARCH_PATTERN = r"^nginx-access-ui\.log-(\d{8})\.(gz|txt)$"
FORMAT_CODE = "%Y%m%d"
LogEntity = namedtuple("LogEntity", ["extension", "date", "filepath"])


def fetch_log_entity(dir_log, logger) -> LogEntity | None:
    logger.info(f"Поиск лог файла в директории: {dir_log}")

    file_entity = None

    for filename in listdir(dir_log):
        absolute_filepath = os.path.join(dir_log, filename)

        if not isfile(absolute_filepath):
            continue

        matcher = re.search(SEARCH_PATTERN, filename)

        if matcher and file_most_resent(matcher, file_entity):
            file_entity = build_entity(matcher, absolute_filepath)
            logger.info(f"Обнаружен лог-кандидат на обработку: {file_entity}")

    logger.info(f"Наиболее актуальный лог на обработку: {file_entity}")
    return file_entity


def file_most_resent(matcher, file_entity):
    if not file_entity:
        return True

    date = parse_date(matcher)
    return date > file_entity.date


def build_entity(matcher, absolute_filepath):
    date = parse_date(matcher)
    extension = matcher.group(2)

    return LogEntity(extension=extension, date=date, filepath=absolute_filepath)


def parse_date(matcher):
    return datetime.strptime(matcher.group(1), FORMAT_CODE)
