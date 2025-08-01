__all__ = ["Parser"]

from typing import List

from src.utils.parser.analytics import build_calculated_analytics
from src.utils.parser.atom import decompose
from src.utils.parser.state import AtomAnalytics, State


class Parser:
    def __init__(self, config):
        self.config = config
        self.state = State()

    """
    Парсит 'атом' лога, 'атомом' является запись относящаяся к одному
    событию из лога.
    """

    def atom_decompose(self, atom_str: str):
        atom = decompose(atom_str)

        if not atom:
            self._process_error(atom_str)
            return

        self._process_decompose(atom)

    def calculate_analytics(self) -> List[AtomAnalytics] | None:
        failed = self.state.atom_global.failed_total
        success = self.state.atom_global.success_total

        if failed > 0:
            total = failed + success
            error_percent = round(failed / total * 100, 5)
            if error_percent - self.config.max_error_percent > 0:
                self.config.logger.error(
                    f"При парсинге лог-файла превышен порог ошибок: {error_percent}%"
                )
                return None

        return build_calculated_analytics(self.state, self.config.report_size)

    def _process_error(self, atom_str):
        self.config.logger.error(f"Ошибка парсинга строки: {atom_str}")
        self.state.atom_global.failed_total += 1

    def _process_decompose(self, atom):
        self.state.atom_global.success_total += 1
        self.state.atom_global.time_total += atom.response_time
        self.state.atom_storage.append(atom)
