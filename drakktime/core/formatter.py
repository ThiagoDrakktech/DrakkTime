from typing import Iterable

from .models import OvertimeSummary
from .utils import format_minutes


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
                    format_minutes(summary.overtime_minutes),
                )
            )
        )

    return "\n".join(lines)
