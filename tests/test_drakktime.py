import unittest

from drakktime import (
    Employee,
    Role,
    SaturdayMode,
    TimeRecord,
    expected_daily_minutes,
    format_summary_table,
    summarize_overtime,
)


class DrakkTimeTests(unittest.TestCase):
    def test_expected_minutes_44h_with_saturday(self):
        employee = Employee(
            first_name="Ana",
            last_name="Silva",
            cpf="00011122233",
            role=Role.GERENTE,
            worked_period="2026-09",
            saturday_mode=SaturdayMode.TODO_SABADO,
        )

        self.assertEqual(expected_daily_minutes(employee, "2026-09-14"), 8 * 60)  # Monday
        self.assertEqual(expected_daily_minutes(employee, "2026-09-19"), 4 * 60)  # Saturday

    def test_extra_return_adds_worked_time(self):
        employee = Employee(
            first_name="João",
            last_name="Souza",
            cpf="12345678901",
            role=Role.ASSISTENTE_ADMINISTRATIVO,
            worked_period="2026-09",
            saturday_mode=SaturdayMode.ALTERNADO,
        )
        record = TimeRecord(
            employee=employee,
            work_date="2026-09-14",
            start_time="08:00",
            lunch_start="12:00",
            lunch_end="13:00",
            end_time="18:00",
            returned_after_end=True,
            extra_start="19:00",
            extra_end="20:30",
        )

        self.assertEqual(record.worked_minutes(), 630)
        self.assertEqual(record.overtime_minutes(), 102)

    def test_summary_table_contains_employee_and_total(self):
        employee = Employee(
            first_name="Maria",
            last_name="Lima",
            cpf="99988877766",
            role=Role.AUXILIAR_MANUTENCAO,
            worked_period="2026-09",
            saturday_mode=SaturdayMode.TODO_SABADO,
        )
        records = [
            TimeRecord(
                employee=employee,
                work_date="2026-09-14",
                start_time="08:00",
                lunch_start="12:00",
                lunch_end="13:00",
                end_time="18:30",
            ),
            TimeRecord(
                employee=employee,
                work_date="2026-09-15",
                start_time="08:00",
                lunch_start="12:00",
                lunch_end="13:00",
                end_time="18:00",
            ),
        ]

        table = format_summary_table(summarize_overtime(records))

        self.assertIn("Maria Lima", table)
        self.assertIn("99988877766", table)
        self.assertIn("02:30", table)


if __name__ == "__main__":
    unittest.main()
