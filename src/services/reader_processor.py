__all__ = ["ReaderProcessor"]

from datetime import datetime

from src.utils.reader_processor.log_file import fetch_log_entity
from src.utils.reader_processor.readers import run_gz_log_reader, run_plain_log_reader

GNU_ZIP_EXTENSION = "gz"


class ReaderProcessor:
    def __init__(self, config, parser):
        self.config = config
        self.parser = parser
        self.logger = self.config.logger

    def run(self) -> datetime | None:
        self.logger.info("Запущен обработчик логов")

        log_entity = fetch_log_entity(self.config.log_dir, self.logger)

        if log_entity:
            self._process_log_file(log_entity)
            return log_entity.date
        else:
            self.logger.info(
                "В указанной директории лог не обнаружен:",
                log_dir=self.config.log_dir,
            )
            return None

    def _process_log_file(self, log_entity):
        if log_entity.extension == GNU_ZIP_EXTENSION:
            run_gz_log_reader(log_entity, self.logger, self.parser)
            return

        run_plain_log_reader(log_entity, self.logger, self.parser, self.config.encoding)
