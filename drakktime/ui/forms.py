"""Componentes de formulários."""

import PySimpleGUI as sg
from datetime import datetime, date
from .styles import PADDING, INPUT_WIDTH, BUTTON_WIDTH, COLOR_PRIMARY


def time_input(key: str, label: str = "Horário") -> list:
    """Campo de entrada de horário (HH:MM)."""
    return [
        sg.Text(label, size=(15, 1), font=("Segoe UI", 10)),
        sg.InputText(
            default_text=datetime.now().strftime("%H:%M"),
            key=key,
            size=(INPUT_WIDTH, 1),
            font=("Segoe UI", 10),
        ),
    ]


def date_input(key: str, label: str = "Data") -> list:
    """Campo de entrada de data."""
    return [
        sg.Text(label, size=(15, 1), font=("Segoe UI", 10)),
        sg.InputText(
            default_text=date.today().isoformat(),
            key=key,
            size=(INPUT_WIDTH, 1),
            font=("Segoe UI", 10),
        ),
    ]


def text_input(key: str, label: str, default: str = "") -> list:
    """Campo de texto simples."""
    return [
        sg.Text(label, size=(15, 1), font=("Segoe UI", 10)),
        sg.InputText(
            default_text=default,
            key=key,
            size=(INPUT_WIDTH, 1),
            font=("Segoe UI", 10),
        ),
    ]


def dropdown(key: str, label: str, values: list, default: str = None) -> list:
    """Dropdown (combobox)."""
    return [
        sg.Text(label, size=(15, 1), font=("Segoe UI", 10)),
        sg.Combo(
            values=values,
            default_value=default or (values[0] if values else ""),
            key=key,
            size=(INPUT_WIDTH - 2, 1),
            font=("Segoe UI", 10),
            readonly=True,
        ),
    ]


def separator() -> list:
    """Linha separadora."""
    return [sg.HorizontalLine(color=COLOR_PRIMARY)]
