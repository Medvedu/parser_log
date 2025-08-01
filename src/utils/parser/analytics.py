__all__ = ["build_calculated_analytics"]

from src.utils.parser.atom import Atom
from src.utils.parser.state import AtomAnalytics, AtomGlobal


def build_calculated_analytics(state, records_count):
    atom_analytics = {}

    for atom in state.atom_storage:
        if atom_analytics.get(atom.path):
            atom_analytics[atom.path] = update_atom_analytics(
                atom, atom_analytics.get(atom.path)
            )
        else:
            atom_analytics[atom.path] = create_atom_analytics(atom)

    top_atom_analytics = build_top_atom_analytics(atom_analytics, records_count)
    enrich_atom_analytics_with_data(top_atom_analytics, state.atom_global)

    return top_atom_analytics


def update_atom_analytics(atom: Atom, atom_analytics: AtomAnalytics):
    count = atom_analytics.count + 1
    time_sum = atom_analytics.time_sum + atom.response_time
    time_max = max(atom_analytics.time_max, atom.response_time)
    # Для больших логов попытка создать избыточные объекты типа "массив"
    # ведет к значительному увеличению времени выполнения скрипта,
    # поэтому далее мутируется стейт существующего объекта.
    atom_analytics.time_history.append(atom.response_time)

    return AtomAnalytics(
        count=count,
        time_sum=time_sum,
        time_max=time_max,
        time_history=atom_analytics.time_history,
        url=atom_analytics.url,
    )


def create_atom_analytics(atom: Atom):
    return AtomAnalytics(
        count=1,
        time_sum=atom.response_time,
        time_max=atom.response_time,
        time_history=[atom.response_time],
        url=atom.path,
    )


def build_top_atom_analytics(atom_analytics, records_count):
    sorted_atom_analytics = sorted(
        atom_analytics.values(), key=lambda x: x.time_sum, reverse=True
    )

    return sorted_atom_analytics[:records_count]


def enrich_atom_analytics_with_data(top_atom_analytics_slice, atom_global: AtomGlobal):
    for entity in top_atom_analytics_slice:
        entity.count_perc = round(entity.count / atom_global.success_total * 100, 2)
        entity.time_perc = round(entity.time_sum / atom_global.time_total * 100, 2)
        entity.time_avg = round(entity.time_sum / entity.count, 2)
        entity.time_med = round(calculate_median(entity), 2)
        entity.time_sum = round(entity.time_sum, 2)


def calculate_median(atom_analytics: AtomAnalytics):
    sorted_times = sorted(atom_analytics.time_history)
    mid = atom_analytics.count // 2

    if atom_analytics.count % 2 == 1:
        return sorted_times[mid]

    return (sorted_times[mid - 1] + sorted_times[mid]) / 2
