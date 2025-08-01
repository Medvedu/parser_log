__all__ = ["State", "AtomAnalytics", "AtomGlobal"]

from dataclasses import dataclass, field
from typing import List

from src.utils.parser.atom import Atom

"""
    * url
        Анализируемый URL;
    * count
        сколько раз встречается URL, абсолютное значение;
    * count_perc
        сколько раз встречается URL, в процентах относительно общего числа
        запросов;
    * time_sum
        суммарный $request_time для данного URL’а, абсолютное значение;
    * time_perc
        суммарный $request_time для данного URL’а, в процентах относительно
        общего $request_time всех запросов;
    * time_avg
        средний $request_time для данного URL’а;
    * time_max
        максимальный $request_time для данного URL’а;
    * time_med
        медиана $request_time для данного URL’а;
    * time_history
        Список времени всех ответов по URL'у, необходимо для вычисления медианы.
"""


@dataclass
class AtomAnalytics:
    url: str | None = None
    count: int = 0
    time_sum: float = 0
    count_perc: float = 0
    time_perc: float = 0
    time_avg: float = 0
    time_max: float = 0
    time_med: float = 0
    time_history: List[float] = field(default_factory=list)

    def to_dict(self):
        return {
            "url": self.url,
            "count": self.count,
            "time_sum": self.time_sum,
            "count_perc": self.count_perc,
            "time_perc": self.time_perc,
            "time_avg": self.time_avg,
            "time_max": self.time_max,
            "time_med": self.time_med,
        }


"""
    * count_total
        Общее количество URL;
    * time_total
        Общее время на запросы;
    * failed_total
        Количество необработанных URL.
"""


@dataclass
class AtomGlobal:
    success_total: int = 0
    time_total: float = 0
    failed_total: int = 0


"""
    * atom_storage
       Хранилище распаршенных строк лога;
    * atom_analytics
        Статистика для отчета;
    * atom_global
        Глобальная статистика.
"""


@dataclass
class State:
    atom_storage: List[Atom] = field(default_factory=list)
    atom_global: AtomGlobal = field(default_factory=AtomGlobal)
    atom_analytics: List[AtomAnalytics] = field(default_factory=list)
