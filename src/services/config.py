__all__ = ["Config"]

import os

from src.utils.config.env_loader import load_env_variables
from src.utils.config.validator import validate


class Config:
    def __init__(self):
        self.service_log_file = None
        self.logger = None
        load_env_variables(self, ".env.local")

    def overload(self, config_path: str):
        if not os.path.exists(config_path):
            print("Конфигурационный файл в системе не обнаружен:", config_path)
            raise FileNotFoundError(config_path)

        load_env_variables(self, config_path)
        validate(self)
