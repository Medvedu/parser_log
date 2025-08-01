from datetime import datetime
from unittest.mock import MagicMock, patch

from src.utils.reader_processor.log_file import FORMAT_CODE, LogEntity, fetch_log_entity


@patch("src.utils.reader_processor.log_file.listdir")
@patch("src.utils.reader_processor.log_file.isfile")
def test_fetch_log_entity_returns_latest_log(mock_isfile, mock_listdir):
    mock_listdir.return_value = [
        "nginx-access-ui.log-20230420.txt",
        "nginx-access-ui.log-20230422.gz",
        "nginx-access-ui.log-20230421.txt",
        "random-file.txt",
    ]

    mock_isfile.return_value = True
    logger = MagicMock()
    result = fetch_log_entity("/fake/dir", logger)

    assert result is not None
    assert isinstance(result, LogEntity)
    assert result.date == datetime.strptime("20230422", FORMAT_CODE)
    assert result.extension == "gz"
    assert result.filepath.endswith("nginx-access-ui.log-20230422.gz")

    logger.info.assert_any_call("Поиск лог файла в директории: /fake/dir")
    logger.info.assert_any_call(f"Обнаружен лог-кандидат на обработку: {result}")
    logger.info.assert_any_call(f"Наиболее актуальный лог на обработку: {result}")
