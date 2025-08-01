__all__ = ["decompose", "Atom"]

import re
from dataclasses import dataclass


@dataclass
class Atom:
    path: str
    response_time: float


"""
    Между полями допускается любое количество пробелов, однако требуется
    соблюдать порядок полей. Полную структуру полей см. в техническом задании.
"""
LOG_PATTERN = re.compile(
    r"^"
    r"(?P<ip>\S+)\s+"
    r"(?P<user_id>\S+)\s+"
    r"-\s+"
    r"\[(?P<time_local>[^\]]+)\]\s+"
    r'"(?P<method>\S+)\s+'
    r"(?P<path>\S+)\s+"
    r'(?P<protocol>[^"]+)"\s+'
    r"(?P<status>\d{3})\s+"
    r"(?P<body_bytes_sent>\d+)\s+"
    r'"[^"]*"\s+'
    r'"[^"]*"\s+'
    r'"[^"]*"\s+'
    r'"[^"]*"\s+'
    r'"[^"]*"\s+'
    r"(?P<request_time>[\d.]+)"
    r"$"
)


"""
Структура строк лога (переменная atom_str), примеры:
    '1.168.229.112 545a7b821307935d  - [29/Jun/2017:04:07:53 +0300] "GET /agency/campaigns/6400337/banners/bulk_read/ HTTP/1.1" 200 79 "-" "python-requests/2.13.0" "-" "1498698472-743364018-4709-9936734" "-" 0.698\n'
    '1.168.229.112 545a7b821307935d  - [29/Jun/2017:04:07:53 +0300] "GET /agency/campaigns/6400337/banners/bulk_read/ HTTP/1.1" 200 79 "-" "python-requests/2.13.0" "-" "1498698472-743364018-4709-9936734" "-" 0.698\n'
    '1.168.229.112 545a7b821307935d  - [29/Jun/2017:04:07:53 +0300] "GET /agency/campaigns/6400337/banners/bulk_read/ HTTP/1.1" 200 79 "-" "python-requests/2.13.0" "-" "1498698472-743364018-4709-9936734" "-" 0.698\n'
    '1.168.229.112 545a7b821307935d  - [29/Jun/2017:04:07:53 +0300] "GET /agency/campaigns/6400337/banners/bulk_read/ HTTP/1.1" 200 79 "-" "python-requests/2.13.0" "-" "1498698472-743364018-4709-9936734" "-" 0.698\n'

"""


def decompose(atom_str: str) -> Atom | None:
    match = LOG_PATTERN.match(atom_str.strip())

    if not match:
        return None

    path = match.group("path")
    response_time_str = match.group("request_time")
    try:
        response_time = float(response_time_str)
    except ValueError:
        return None

    return Atom(path=path, response_time=response_time)
