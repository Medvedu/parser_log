__all__ = ["run_gz_log_reader", "run_plain_log_reader"]

import gzip


def run_gz_log_reader(log_entity, logger, parser):
    logger.info(f"Чтение сжатого gzip-файла: {log_entity.filepath}")
    try:
        with gzip.open(log_entity.filepath, "rt") as gz_file:
            for line in gz_file:
                parser.atom_decompose(line)
        logger.info("Чтение gzip-файла завершено успешно")
    except (OSError, IOError, EOFError) as e:
        logger.error(f"Ошибка при чтении gzip-файла: {e}")


def run_plain_log_reader(log_entity, logger, parser, encoding):
    logger.info(f"Чтение лог файла: {log_entity.filepath}")

    try:
        with open(log_entity.filepath, "r", encoding=encoding) as plain_file:
            for line in plain_file:
                parser.atom_decompose(line)
        logger.info("Чтение лог-файла завершено успешно")
    except (OSError, IOError) as e:
        logger.error(f"Ошибка при чтении лог-файла: {e}")
