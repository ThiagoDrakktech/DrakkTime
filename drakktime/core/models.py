from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Role(str, Enum):
    GERENTE = "Gerente"
    ASSISTENTE_ADMINISTRATIVO = "Assistente Administrativo"
    OFICIAL_MANUTENCAO = "Oficial de Manutenção"
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
    registration_date: str
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


@dataclass(frozen=True)
class OvertimeSummary:
    employee: Employee
    overtime_minutes: int
