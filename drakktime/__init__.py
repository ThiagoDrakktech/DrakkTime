"""DrakkTime - Sistema de cálculo de horas extras."""

from .core import (
    Employee,
    OvertimeSummary,
    Role,
    SaturdayMode,
    TimeRecord,
    calculate_overtime_minutes,
    calculate_worked_minutes,
    expected_daily_minutes,
    format_summary_table,
    summarize_overtime,
)

__version__ = "0.1.0"

__all__ = [
    "Employee",
    "TimeRecord",
    "OvertimeSummary",
    "Role",
    "SaturdayMode",
    "expected_daily_minutes",
    "calculate_worked_minutes",
    "calculate_overtime_minutes",
    "summarize_overtime",
    "format_summary_table",
]
