from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Iterable, Optional


class Role(str, Enum):
    GERENTE = "Gerente"
    ASSISTENTE_ADMINISTRATIVO = "Assistente Administrativo"
    OFICIAL_MANUTENCAO = "Oficial de manutenção"
    AUXILIAR_MANUTENCAO = "Auxiliar de Manutenção"


class SaturdayMode(str, Enum):
    ALTERNADO = "alternado"
    TODO_SABADO = "todo_sabado"


@dataclass(frozen=True)
class Employee:
    first_name: str
    last_name: str
    cpf: str
    role: Role
    worked_period: str
    saturday_mode: SaturdayMode = SaturdayMode.ALTERNADO

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


@dataclass(frozen=True)
class TimeRecord:
    employee: Employee
    work_date: str
    start_time: str
    lunch_start: str
    lunch_end: str
    end_time: str
    returned_after_end: bool = False
    extra_start: Optional[str] = None
    extra_end: Optional[str] = None

    def worked_minutes(self) -> int:
        start = _parse_time(self.start_time)
        lunch_start = _parse_time(self.lunch_start)
        lunch_end = _parse_time(self.lunch_end)
        end = _parse_time(self.end_time)

        if not (start <= lunch_start <= lunch_end <= end):
            raise ValueError("Horários principais inválidos")

        regular_minutes = _minutes_between(start, lunch_start) + _minutes_between(lunch_end, end)

        if not self.returned_after_end:
            return regular_minutes

        if not self.extra_start or not self.extra_end:
            raise ValueError("Retorno pós-expediente requer horário de retorno e baixa")

        extra_start = _parse_time(self.extra_start)
        extra_end = _parse_time(self.extra_end)
        if not (end <= extra_start <= extra_end):
            raise ValueError("Horários de retorno pós-expediente inválidos")

        return regular_minutes + _minutes_between(extra_start, extra_end)

    def overtime_minutes(self) -> int:
        expected = expected_daily_minutes(self.employee, self.work_date)
        return max(0, self.worked_minutes() - expected)


@dataclass(frozen=True)
class OvertimeSummary:
    employee: Employee
    overtime_minutes: int


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


def summarize_overtime(records: Iterable[TimeRecord]) -> list[OvertimeSummary]:
    totals: dict[str, tuple[Employee, int]] = {}

    for record in records:
        key = record.employee.cpf
        employee, total = totals.get(key, (record.employee, 0))
        totals[key] = (employee, total + record.overtime_minutes())

    return [
        OvertimeSummary(employee=employee, overtime_minutes=overtime)
        for employee, overtime in totals.values()
    ]


def format_summary_table(summaries: Iterable[OvertimeSummary]) -> str:
    headers = ("Colaborador", "CPF", "Cargo", "Horas Extras")
    lines = [" | ".join(headers), " | ".join("-" * len(h) for h in headers)]

    for summary in summaries:
        lines.append(
            " | ".join(
                (
                    summary.employee.full_name,
                    summary.employee.cpf,
                    summary.employee.role.value,
                    _format_minutes(summary.overtime_minutes),
                )
            )
        )

    return "\n".join(lines)


def _parse_time(value: str) -> datetime:
    return datetime.strptime(value, "%H:%M")


def _minutes_between(start: datetime, end: datetime) -> int:
    return int((end - start).total_seconds() // 60)


def _format_minutes(total_minutes: int) -> str:
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours:02d}:{minutes:02d}"


if __name__ == "__main__":
    print("DrakkTime - cálculo de horas extras")
    print("Use este módulo em integração com interface desktop/web conforme necessidade.")
