"""Janela principal da aplicação."""

from datetime import datetime, date
from typing import Optional
import PySimpleGUI as sg

from drakktime.core import (
    Employee,
    TimeRecord,
    Role,
    SaturdayMode,
    calculate_overtime_minutes,
    summarize_overtime,
    format_summary_table,
)
from .styles import COLOR_PRIMARY, COLOR_SUCCESS, COLOR_DANGER, PADDING, INPUT_WIDTH, BUTTON_WIDTH
from .forms import time_input, date_input, text_input, dropdown, separator


class DrakkTimeUI:
    def __init__(self):
        self.employees: dict[str, Employee] = {}
        self.records: list[TimeRecord] = []
        self.setup_theme()

    def setup_theme(self):
        """Configura o tema visual."""
        sg.theme("DarkBlue3")
        sg.set_options(
            font=("Segoe UI", 10),
            element_padding=PADDING,
            margins=(10, 10),
        )

    def create_employee_tab(self) -> sg.Tab:
        """Aba para gerenciar funcionários."""
        layout = [
            [sg.Text("Gerenciar Funcionários", font=("Segoe UI", 14, "bold"))],
            [sg.HorizontalLine()],
            [
                sg.Text("Nome:", size=(12, 1)),
                sg.InputText(key="-EMP_FIRST_NAME-", size=(INPUT_WIDTH, 1)),
            ],
            [
                sg.Text("Sobrenome:", size=(12, 1)),
                sg.InputText(key="-EMP_LAST_NAME-", size=(INPUT_WIDTH, 1)),
            ],
            [
                sg.Text("CPF:", size=(12, 1)),
                sg.InputText(key="-EMP_CPF-", size=(INPUT_WIDTH, 1)),
            ],
            [
                sg.Text("Cargo:", size=(12, 1)),
                sg.Combo(
                    values=[r.value for r in Role],
                    key="-EMP_ROLE-",
                    size=(INPUT_WIDTH - 2, 1),
                    readonly=True,
                ),
            ],
            [
                sg.Text("Período Trabalhado:", size=(12, 1)),
                sg.InputText(key="-EMP_PERIOD-", size=(INPUT_WIDTH, 1), default_text="2024-01"),
            ],
            [
                sg.Text("Modo Sábado:", size=(12, 1)),
                sg.Combo(
                    values=[s.value for s in SaturdayMode],
                    key="-EMP_SATURDAY-",
                    size=(INPUT_WIDTH - 2, 1),
                    readonly=True,
                    default_value=SaturdayMode.ALTERNADO.value,
                ),
            ],
            [
                sg.Button("➕ Adicionar Funcionário", key="-ADD_EMPLOYEE-", size=(20, 1)),
                sg.Button("🗑️ Remover", key="-REMOVE_EMPLOYEE-", size=(12, 1)),
            ],
            [sg.HorizontalLine()],
            [
                sg.Listbox(
                    values=[],
                    key="-EMPLOYEE_LIST-",
                    size=(40, 10),
                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                )
            ],
        ]
        return sg.Tab("👤 Funcionários", layout, key="-TAB_EMPLOYEES-")

    def create_timesheet_tab(self) -> sg.Tab:
        """Aba para registrar ponto."""
        layout = [
            [sg.Text("Registrar Ponto", font=("Segoe UI", 14, "bold"))],
            [sg.HorizontalLine()],
            [
                sg.Text("Funcionário:", size=(12, 1)),
                sg.Combo(
                    values=[],
                    key="-TIMESHEET_EMPLOYEE-",
                    size=(INPUT_WIDTH - 2, 1),
                    readonly=True,
                ),
            ],
            [
                sg.Text("Data:", size=(12, 1)),
                sg.InputText(
                    default_text=date.today().isoformat(),
                    key="-TIMESHEET_DATE-",
                    size=(INPUT_WIDTH, 1),
                ),
            ],
            [sg.Text("Horários do Expediente:", font=("Segoe UI", 11, "bold"))],
            [
                sg.Text("Entrada:", size=(12, 1)),
                sg.InputText(key="-START_TIME-", size=(INPUT_WIDTH, 1), default_text="08:00"),
            ],
            [
                sg.Text("Início Almoço:", size=(12, 1)),
                sg.InputText(key="-LUNCH_START-", size=(INPUT_WIDTH, 1), default_text="12:00"),
            ],
            [
                sg.Text("Fim Almoço:", size=(12, 1)),
                sg.InputText(key="-LUNCH_END-", size=(INPUT_WIDTH, 1), default_text="13:00"),
            ],
            [
                sg.Text("Saída:", size=(12, 1)),
                sg.InputText(key="-END_TIME-", size=(INPUT_WIDTH, 1), default_text="17:00"),
            ],
            [
                sg.Checkbox(
                    "Retornou após expediente?",
                    key="-RETURNED_AFTER-",
                    default=False,
                )
            ],
            [
                sg.Text("Retorno - Entrada:", size=(12, 1)),
                sg.InputText(key="-EXTRA_START-", size=(INPUT_WIDTH, 1), disabled=True),
            ],
            [
                sg.Text("Retorno - Saída:", size=(12, 1)),
                sg.InputText(key="-EXTRA_END-", size=(INPUT_WIDTH, 1), disabled=True),
            ],
            [
                sg.Button("💾 Registrar Ponto", key="-SAVE_RECORD-", size=(20, 1)),
            ],
            [sg.HorizontalLine()],
            [sg.Text("Registros Hoje:", font=("Segoe UI", 11, "bold"))],
            [
                sg.Listbox(
                    values=[],
                    key="-RECORDS_LIST-",
                    size=(40, 8),
                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                )
            ],
            [sg.Button("🗑️ Remover Registro", key="-REMOVE_RECORD-", size=(12, 1))],
        ]
        return sg.Tab("⏱️ Ponto", layout, key="-TAB_TIMESHEET-")

    def create_summary_tab(self) -> sg.Tab:
        """Aba para visualizar resumo de horas extras."""
        layout = [
            [sg.Text("Resumo de Horas Extras", font=("Segoe UI", 14, "bold"))],
            [sg.HorizontalLine()],
            [
                sg.Text("Período:", size=(12, 1)),
                sg.InputText(
                    default_text="2024-01",
                    key="-SUMMARY_PERIOD-",
                    size=(INPUT_WIDTH, 1),
                ),
            ],
            [
                sg.Button("🔄 Atualizar", key="-REFRESH_SUMMARY-", size=(12, 1)),
                sg.Button("📊 Exportar CSV", key="-EXPORT_CSV-", size=(14, 1)),
            ],
            [sg.HorizontalLine()],
            [
                sg.Multiline(
                    size=(50, 15),
                    key="-SUMMARY_OUTPUT-",
                    disabled=True,
                    font=("Courier New", 10),
                )
            ],
        ]
        return sg.Tab("📊 Resumo", layout, key="-TAB_SUMMARY-")

    def create_layout(self) -> list:
        """Cria o layout principal."""
        tabgroup = sg.TabGroup(
            [
                [
                    self.create_employee_tab(),
                    self.create_timesheet_tab(),
                    self.create_summary_tab(),
                ]
            ],
            key="-TABGROUP-",
            pad=(0, 0),
        )

        layout = [
            [sg.Text("🕐 DrakkTime", font=("Segoe UI", 16, "bold"), text_color=COLOR_PRIMARY)],
            [sg.Text("Sistema de Controle de Horas Extras", font=("Segoe UI", 10))],
            [sg.HorizontalLine()],
            [tabgroup],
            [sg.HorizontalLine()],
            [
                sg.Text("v0.1.0", font=("Segoe UI", 9), text_color="#999999"),
                sg.Push(),
                sg.Button("❌ Sair", key="-EXIT-", size=(10, 1)),
            ],
        ]

        return layout

    def run(self):
        """Executa a interface."""
        window = sg.Window("DrakkTime - Controle de Horas", self.create_layout(), finalize=True)

        # Variáveis de estado
        selected_employee_index = None
        selected_record_index = None

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == "-EXIT-":
                break

            # ===== TAB FUNCIONÁRIOS =====
            elif event == "-ADD_EMPLOYEE-":
                try:
                    if not values["-EMP_FIRST_NAME-"] or not values["-EMP_CPF-"]:
                        sg.popup_error("❌ Preencha nome e CPF!")
                        continue

                    emp = Employee(
                        first_name=values["-EMP_FIRST_NAME-"],
                        last_name=values["-EMP_LAST_NAME-"],
                        cpf=values["-EMP_CPF-"],
                        role=Role(values["-EMP_ROLE-"]) if values["-EMP_ROLE-"] else Role.ASSISTENTE_ADMINISTRATIVO,
                        worked_period=values["-EMP_PERIOD-"],
                        saturday_mode=SaturdayMode(values["-EMP_SATURDAY-"]),
                    )
                    self.employees[emp.cpf] = emp
                    self._update_employee_list(window)
                    self._update_timesheet_dropdown(window)
                    sg.popup_ok(f"✅ {emp.full_name} adicionado com sucesso!")

                    # Limpar formulário
                    window["-EMP_FIRST_NAME-"].update("")
                    window["-EMP_LAST_NAME-"].update("")
                    window["-EMP_CPF-"].update("")
                    window["-EMP_ROLE-"].update("")

                except Exception as e:
                    sg.popup_error(f"❌ Erro: {str(e)}")

            elif event == "-REMOVE_EMPLOYEE-":
                list_index = values["-EMPLOYEE_LIST-"]
                if list_index:
                    cpf = list(self.employees.keys())[list_index[0]]
                    emp = self.employees.pop(cpf)
                    self._update_employee_list(window)
                    self._update_timesheet_dropdown(window)
                    sg.popup_ok(f"🗑️ {emp.full_name} removido!")

            # ===== TAB PONTO =====
            elif event == "-RETURNED_AFTER-":
                is_checked = values["-RETURNED_AFTER-"]
                window["-EXTRA_START-"].update(disabled=not is_checked)
                window["-EXTRA_END-"].update(disabled=not is_checked)

            elif event == "-SAVE_RECORD-":
                try:
                    emp_name = values["-TIMESHEET_EMPLOYEE-"]
                    if not emp_name:
                        sg.popup_error("❌ Selecione um funcionário!")
                        continue

                    # Encontrar funcionário
                    employee = None
                    for emp in self.employees.values():
                        if emp.full_name == emp_name:
                            employee = emp
                            break

                    if not employee:
                        sg.popup_error("❌ Funcionário não encontrado!")
                        continue

                    record = TimeRecord(
                        employee=employee,
                        work_date=values["-TIMESHEET_DATE-"],
                        start_time=values["-START_TIME-"],
                        lunch_start=values["-LUNCH_START-"],
                        lunch_end=values["-LUNCH_END-"],
                        end_time=values["-END_TIME-"],
                        returned_after_end=values["-RETURNED_AFTER-"],
                        extra_start=values["-EXTRA_START-"] if values["-RETURNED_AFTER-"] else None,
                        extra_end=values["-EXTRA_END-"] if values["-RETURNED_AFTER-"] else None,
                    )
                    self.records.append(record)
                    self._update_records_list(window)
                    sg.popup_ok("✅ Ponto registrado com sucesso!")

                except Exception as e:
                    sg.popup_error(f"❌ Erro: {str(e)}")

            elif event == "-REMOVE_RECORD-":
                if values["-RECORDS_LIST-"]:
                    idx = values["-RECORDS_LIST-"][0]
                    self.records.pop(idx)
                    self._update_records_list(window)
                    sg.popup_ok("🗑️ Registro removido!")

            # ===== TAB RESUMO =====
            elif event == "-REFRESH_SUMMARY-":
                try:
                    summaries = summarize_overtime(self.records)
                    table = format_summary_table(summaries) if summaries else "Nenhum registro encontrado."
                    window["-SUMMARY_OUTPUT-"].update(table)
                except Exception as e:
                    window["-SUMMARY_OUTPUT-"].update(f"❌ Erro: {str(e)}")

            elif event == "-EXPORT_CSV-":
                try:
                    summaries = summarize_overtime(self.records)
                    if not summaries:
                        sg.popup_error("❌ Nenhum dado para exportar!")
                        continue

                    file_path = sg.popup_get_file(
                        "Salvar como:",
                        save_as=True,
                        file_types=(("CSV Files", "*.csv"),),
                        default_extension=".csv",
                    )

                    if file_path:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write("Colaborador,CPF,Cargo,Horas Extras\n")
                            for summary in summaries:
                                hours, minutes = divmod(summary.overtime_minutes, 60)
                                f.write(
                                    f"{summary.employee.full_name},{summary.employee.cpf},"
                                    f"{summary.employee.role.value},{hours:02d}:{minutes:02d}\n"
                                )
                        sg.popup_ok(f"✅ Exportado para: {file_path}")

                except Exception as e:
                    sg.popup_error(f"❌ Erro ao exportar: {str(e)}")

        window.close()

    def _update_employee_list(self, window):
        """Atualiza a listbox de funcionários."""
        emp_list = [emp.full_name for emp in self.employees.values()]
        window["-EMPLOYEE_LIST-"].update(emp_list)

    def _update_timesheet_dropdown(self, window):
        """Atualiza o dropdown de funcionários no timesheet."""
        emp_list = [emp.full_name for emp in self.employees.values()]
        window["-TIMESHEET_EMPLOYEE-"].update(values=emp_list)

    def _update_records_list(self, window):
        """Atualiza a listbox de registros."""
        records_display = []
        for record in self.records:
            records_display.append(
                f"{record.work_date} | {record.employee.full_name} | "
                f"{record.start_time} → {record.end_time}"
            )
        window["-RECORDS_LIST-"].update(records_display)


def main():
    """Ponto de entrada da UI."""
    app = DrakkTimeUI()
    app.run()


if __name__ == "__main__":
    main()
