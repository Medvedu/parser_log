import pytest

from src.utils.parser.atom import Atom, decompose


def test_decompose_valid_line():
    line = (
        "1.168.229.112 545a7b821307935d  - [29/Jun/2017:04:07:53 +0300] "
        '"GET /agency/campaigns/6400337/banners/bulk_read/ HTTP/1.1" 200 79 '
        '"-" "python-requests/2.13.0" "-" "1498698472-743364018-4709-9936734" "-" 0.698\n'
    )

    atom = decompose(line)

    assert atom is not None
    assert isinstance(atom, Atom)
    assert atom.path == "/agency/campaigns/6400337/banners/bulk_read/"
    assert abs(atom.response_time - 0.698) < 1e-6


def test_decompose_line_with_extra_spaces():
    line = (
        "1.168.229.112    545a7b821307935d  -    [29/Jun/2017:04:07:53 +0300] "
        '"GET    /test/path HTTP/1.1" 200 79 "-" "python-requests/2.13.0" "-" '
        '"id" "-" 1.234\n'
    )

    atom = decompose(line)

    assert atom is not None
    assert atom.path == "/test/path"
    assert abs(atom.response_time - 1.234) < 1e-6


@pytest.mark.parametrize(
    "invalid_line",
    [
        "",  # пустая строка
        "just some random text",
        '1.1.1.1 user - [date] "GET /path HTTP/1.1" 200 79 "-" "-" "-" "-" "-" not_a_number',
        '1.1.1.1 user - [date] "GET /path HTTP/1.1" 200 79 "-" "-" "-" "-" "-"',
        '1.1.1.1 user - [date] "GET" 200 79 "-" "-" "-" "-" "-" 0.123',
    ],
)
def test_decompose_invalid_lines_return_none(invalid_line):
    assert decompose(invalid_line) is None


def test_atom_dataclass_fields():
    atom = Atom(path="/some/path", response_time=0.5)
    assert atom.path == "/some/path"
    assert atom.response_time == 0.5
