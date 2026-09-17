from datetime import datetime
from typing import Iterable

from .models import Employee, OvertimeSummary, Role, SaturdayMode, TimeRecord
from .utils import minutes_between, parse_time


def expected_daily_minutes(employee: Employee, work_date: str) -> int:
    week_day = datetime.strptime(work_date, "%Y-%m-%d").weekday()  # 0 = Monday, 5 = Saturday

    if employee.role == Role.OFICIAL_MANUTENCAO:
        return 12 * 60

    if week_day == 6:  # Sunday
        return 0

    if week_day == 5:  # Saturday
        if employee.saturday_mode == SaturdayMode.TODO_SABADO:
            return 4 * 60
        return 0

    # 44h semanais
    if employee.saturday_mode == SaturdayMode.TODO_SABADO:
        return 8 * 60

    # compensação para alternar sábado
    return 8 * 60 + 48


def calculate_worked_minutes(record: TimeRecord) -> int:
    start = parse_time(record.start_time)
    lunch_start = parse_time(record.lunch_start)
    lunch_end = parse_time(record.lunch_end)
    end = parse_time(record.end_time)

    if not (start <= lunch_start <= lunch_end <= end):
        raise ValueError("Horários principais inválidos")

    regular_minutes = minutes_between(start, lunch_start) + minutes_between(lunch_end, end)

    if not record.returned_after_end:
        return regular_minutes

    if not record.extra_start or not record.extra_end:
        raise ValueError("Retorno pós-expediente requer horário de retorno e baixa")

    extra_start = parse_time(record.extra_start)
    extra_end = parse_time(record.extra_end)
    if not (end <= extra_start <= extra_end):
        raise ValueError("Horários de retorno pós-expediente inválidos")

    return regular_minutes + minutes_between(extra_start, extra_end)


def calculate_overtime_minutes(record: TimeRecord) -> int:
    expected = expected_daily_minutes(record.employee, record.work_date)
    return max(0, calculate_worked_minutes(record) - expected)


def summarize_overtime(records: Iterable[TimeRecord]) -> list[OvertimeSummary]:
    totals: dict[str, tuple[Employee, int]] = {}

    for record in records:
        key = record.employee.cpf
        employee, total = totals.get(key, (record.employee, 0))
        totals[key] = (employee, total + calculate_overtime_minutes(record))

    return [
        OvertimeSummary(employee=employee, overtime_minutes=overtime)
        for employee, overtime in totals.values()
    ]
