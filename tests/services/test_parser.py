from unittest.mock import MagicMock, patch

import pytest

from src.services.parser import Parser


@pytest.fixture
def config_mock():
    config = MagicMock()
    config.max_error_percent = 10.0
    config.report_size = 5
    config.logger = MagicMock()
    return config


def test_atom_decompose_calls_process_decompose(config_mock):
    parser = Parser(config_mock)

    fake_atom = MagicMock()
    fake_atom.response_time = 1.23

    with patch(
        "src.services.parser.decompose", return_value=fake_atom
    ) as mock_decompose, patch.object(
        parser, "_process_decompose"
    ) as mock_process_decompose, patch.object(
        parser, "_process_error"
    ) as mock_process_error:

        parser.atom_decompose("valid_atom_string")

        mock_decompose.assert_called_once_with("valid_atom_string")
        mock_process_decompose.assert_called_once_with(fake_atom)
        mock_process_error.assert_not_called()


def test_atom_decompose_calls_process_error_on_none(config_mock):
    parser = Parser(config_mock)

    with patch(
        "src.services.parser.decompose", return_value=None
    ) as mock_decompose, patch.object(
        parser, "_process_error"
    ) as mock_process_error, patch.object(
        parser, "_process_decompose"
    ) as mock_process_decompose:

        parser.atom_decompose("invalid_atom_string")

        mock_decompose.assert_called_once_with("invalid_atom_string")
        mock_process_error.assert_called_once_with("invalid_atom_string")
        mock_process_decompose.assert_not_called()


def test_process_error_increments_failed_and_logs(config_mock):
    parser = Parser(config_mock)
    initial_failed = parser.state.atom_global.failed_total

    parser._process_error("bad_string")

    config_mock.logger.error.assert_called_once_with(
        "Ошибка парсинга строки: bad_string"
    )
    assert parser.state.atom_global.failed_total == initial_failed + 1


def test_process_decompose_increments_success_and_updates_time(config_mock):
    parser = Parser(config_mock)
    initial_success = parser.state.atom_global.success_total
    initial_time = parser.state.atom_global.time_total

    fake_atom = MagicMock()
    fake_atom.response_time = 2.5

    parser._process_decompose(fake_atom)

    assert parser.state.atom_global.success_total == initial_success + 1
    assert parser.state.atom_global.time_total == initial_time + 2.5
    assert fake_atom in parser.state.atom_storage


def test_calculate_analytics_returns_none_if_error_percent_exceeded(config_mock):
    parser = Parser(config_mock)

    parser.state.atom_global.failed_total = 3
    parser.state.atom_global.success_total = 1
    config_mock.max_error_percent = 50

    config_mock.logger.error.reset_mock()

    result = parser.calculate_analytics()

    config_mock.logger.error.assert_called_once()
    assert result is None


def test_calculate_analytics_calls_build_calculated_analytics(config_mock):
    parser = Parser(config_mock)

    parser.state.atom_global.failed_total = 1
    parser.state.atom_global.success_total = 9
    config_mock.max_error_percent = 20

    fake_result = ["analytics1", "analytics2"]

    with patch(
        "src.services.parser.build_calculated_analytics", return_value=fake_result
    ) as mock_build:
        result = parser.calculate_analytics()

        mock_build.assert_called_once_with(parser.state, config_mock.report_size)
        assert result == fake_result
