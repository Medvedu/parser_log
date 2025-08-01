__all__ = ["Application"]

from src.services.config import Config
from src.services.logger_resolver import LoggerResolver
from src.services.parser import Parser
from src.services.publisher import Publisher
from src.services.reader_processor import ReaderProcessor
from src.utils.application.report import build_report


class Application:
    def __init__(self, cli_arguments):
        self.cli_arguments = cli_arguments
        self.config = Config()
        self.parser = Parser(self.config)

    def run(self):
        if self.cli_arguments.config:
            self.config.overload(config_path=self.cli_arguments.config)

        LoggerResolver(self.config).resolve()

        build_report(
            self._reader_processor(), self._publisher(), self.parser, self.config
        )

    def _reader_processor(self):
        return ReaderProcessor(config=self.config, parser=self.parser)

    def _publisher(self):
        return Publisher(self.config)
