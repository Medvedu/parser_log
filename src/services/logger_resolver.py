__all__ = ["LoggerResolver"]

import json
import os

import structlog

from src.utils.logger_resolver.handlers import (
    configure_root_logger,
    fetch_console_handler,
    fetch_file_handler,
)


class LoggerResolver:
    def __init__(self, config):
        self.config = config

    def resolve(self):
        handler = self._resolve_handler()
        configure_root_logger(handler)

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer(
                    serializer=lambda obj, **kw: json.dumps(obj, ensure_ascii=False)
                ),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
        )

        self.config.logger = structlog.get_logger()

    def _resolve_handler(self):
        if self.config.service_log_file:
            self._create_service_log_file_if_not_exists()
            return fetch_file_handler(
                self.config.service_log_file, self.config.encoding
            )

        return fetch_console_handler()

    def _create_service_log_file_if_not_exists(self):
        if not os.path.exists(self.config.service_log_file):
            with open(
                self.config.service_log_file, "w", encoding=self.config.encoding
            ) as _file:
                pass
