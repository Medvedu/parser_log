__all__ = ["load_env_variables"]

import os

from dotenv import load_dotenv


def load_env_variables(config, config_path: str):
    load_dotenv(dotenv_path=config_path)

    if report_size := os.getenv("REPORT_SIZE"):
        try:
            config.report_size = int(report_size)
        except ValueError:
            print(f"Ошибка: Не удалось преобразовать '{report_size}' в целое число.")
            raise TypeError(config.report_size)

    if max_error_percent := os.getenv("MAX_ERROR_PERCENT"):
        try:
            config.max_error_percent = float(max_error_percent)
        except ValueError:
            print(
                f"Ошибка: Не удалось преобразовать '{max_error_percent}' в вещественное число."
            )
            raise TypeError(config.max_error_percent)

    if os.getenv("REPORT_DIR"):
        config.report_dir = os.path.expanduser(str(os.getenv("REPORT_DIR")))

    if os.getenv("LOG_DIR"):
        config.log_dir = os.path.expanduser(str(os.getenv("LOG_DIR")))

    if os.getenv("ENCODING"):
        config.encoding = os.getenv("ENCODING")

    if os.getenv("SERVICE_LOG_FILE"):
        config.service_log_file = os.path.expanduser(str(os.getenv("SERVICE_LOG_FILE")))
