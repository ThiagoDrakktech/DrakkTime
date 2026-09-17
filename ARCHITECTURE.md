# 📁 Estrutura do Projeto DrakkTime

O projeto está organizado em **camadas** para facilitar manutenção, testes e evolução:

```
drakktime/
├── core/              # 🎯 Núcleo - Lógica de negócio
│   ├── __init__.py
│   ├── models.py      # Dataclasses: Employee, TimeRecord, OvertimeSummary
│   ├── calculator.py  # Funções de cálculo: expected_daily_minutes(), calculate_overtime_minutes(), etc
│   ├── formatter.py   # Formatação de saída: format_summary_table()
│   └── utils.py       # Funções auxiliares: parse_time(), minutes_between(), format_minutes()
│
├── ui/                # 🖥️ Interface - Desktop/Web (a ser implementada)
│   └── __init__.py
│
├── config/            # ⚙️ Configuração - JSON/YAML
│   └── __init__.py
│
├── assets/            # 🎨 Recursos - Ícones, estilos
│   └── __init__.py
│
├── __init__.py        # Exportações públicas da API
├── __main__.py        # Ponto de entrada (python -m drakktime)
```

## 📚 Camadas

### Core (Lógica de Negócio)
Contém toda a lógica de cálculo e regras de negócio:
- **models.py**: Definição de estruturas de dados
- **calculator.py**: Funções de cálculo de horas
- **formatter.py**: Formatação para apresentação
- **utils.py**: Utilidades privadas

### UI (Interface)
Separada do core, importa apenas de `core`:
- Desktop: tkinter, Qt, etc.
- Web: Flask, Django, FastAPI, etc.

### Config (Configurações)
Parâmetros de aplicação:
- Regras de cálculo
- Configurações de UI
- Dados de funcionários

### Assets (Recursos)
- Ícones
- Estilos CSS
- Templates HTML

## 🔌 Como Usar

```python
from drakktime import (
    Employee, TimeRecord, Role, SaturdayMode,
    calculate_overtime_minutes, format_summary_table
)

# Criar um funcionário
employee = Employee(
    first_name="João",
    last_name="Silva",
    cpf="123.456.789-00",
    role=Role.GERENTE,
    worked_period="2024-01"
)

# Registrar ponto
record = TimeRecord(
    employee=employee,
    work_date="2024-01-15",
    start_time="08:00",
    lunch_start="12:00",
    lunch_end="13:00",
    end_time="17:00"
)

# Calcular horas extras
overtime = calculate_overtime_minutes(record)
```

## 🚀 Próximos Passos

1. Criar interface de usuário em `ui/`
2. Implementar persistência de dados em `config/`
3. Adicionar testes unitários
4. Integrar com banco de dados
