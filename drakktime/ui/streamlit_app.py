"""Interface Streamlit - Moderna, Responsiva e Persistente"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
from io import StringIO

from drakktime.core import (
    Employee,
    TimeRecord,
    Role,
    SaturdayMode,
    calculate_overtime_minutes,
    summarize_overtime,
)

# ===== CAMINHO DE DADOS =====
DATA_DIR = ".drakktime_data"
EMPLOYEES_FILE = os.path.join(DATA_DIR, "employees.json")
RECORDS_FILE = os.path.join(DATA_DIR, "records.json")

os.makedirs(DATA_DIR, exist_ok=True)

# ===== FUNÇÕES DE PERSISTÊNCIA =====
def salvar_funcionarios():
    """Salva funcionários em JSON."""
    data = {}
    for cpf, emp in st.session_state.employees.items():
        data[cpf] = {
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "cpf": emp.cpf,
            "role": emp.role.value,
            "registration_date": emp.registration_date,
            "saturday_mode": emp.saturday_mode.value,
        }
    with open(EMPLOYEES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def carregar_funcionarios():
    """Carrega funcionários do JSON."""
    if os.path.exists(EMPLOYEES_FILE):
        try:
            with open(EMPLOYEES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for cpf, emp_data in data.items():
                # Migração: se tem worked_period, converter para registration_date
                registration_date = emp_data.get("registration_date") or emp_data.get("worked_period") or "2024-01-01"

                emp = Employee(
                    first_name=emp_data["first_name"],
                    last_name=emp_data["last_name"],
                    cpf=emp_data["cpf"],
                    role=Role(emp_data["role"]),
                    registration_date=registration_date,
                    saturday_mode=SaturdayMode(emp_data["saturday_mode"]),
                )
                st.session_state.employees[cpf] = emp
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar funcionários: {str(e)}")
            pass

def salvar_registros():
    """Salva registros em JSON."""
    data = []
    for rec in st.session_state.records:
        data.append({
            "employee_cpf": rec.employee.cpf,
            "work_date": rec.work_date,
            "start_time": rec.start_time,
            "lunch_start": rec.lunch_start,
            "lunch_end": rec.lunch_end,
            "end_time": rec.end_time,
            "returned_after_end": rec.returned_after_end,
            "extra_start": rec.extra_start,
            "extra_end": rec.extra_end,
        })
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def carregar_registros():
    """Carrega registros do JSON."""
    if os.path.exists(RECORDS_FILE):
        try:
            with open(RECORDS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for rec_data in data:
                # Encontrar funcionário
                cpf = rec_data["employee_cpf"]
                if cpf in st.session_state.employees:
                    emp = st.session_state.employees[cpf]
                    rec = TimeRecord(
                        employee=emp,
                        work_date=rec_data["work_date"],
                        start_time=rec_data["start_time"],
                        lunch_start=rec_data["lunch_start"],
                        lunch_end=rec_data["lunch_end"],
                        end_time=rec_data["end_time"],
                        returned_after_end=rec_data["returned_after_end"],
                        extra_start=rec_data["extra_start"],
                        extra_end=rec_data["extra_end"],
                    )
                    st.session_state.records.append(rec)
        except:
            pass

# ===== CONFIGURAÇÃO PÁGINA =====
st.set_page_config(
    page_title="DrakkTime",
    page_icon="🕐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS para sidebar MUITO MAIOR
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        min-width: 350px !important;
        max-width: 450px !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
    [data-testid="stSidebar"] h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
    }
    [data-testid="stSidebar"] h3 {
        font-size: 1.3rem !important;
        margin: 1.5rem 0 1rem 0 !important;
    }
    [data-testid="stSidebar"] .stRadio {
        padding: 1rem 0 !important;
    }
    [data-testid="stSidebar"] .stRadio > label {
        font-size: 1.4rem !important;
        padding: 1.2rem 0.8rem !important;
        height: 60px !important;
        display: flex !important;
        align-items: center !important;
    }
    [data-testid="stSidebar"] .stRadio > label span {
        font-size: 1.2rem !important;
    }
    [data-testid="stSidebar"] .stMetric {
        background-color: rgba(250, 250, 250, 0.5);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ===== INICIALIZAR SESSION STATE =====
if "employees" not in st.session_state:
    st.session_state.employees = {}
    carregar_funcionarios()

if "records" not in st.session_state:
    st.session_state.records = []
    carregar_registros()

# ===== SIDEBAR MENU =====
with st.sidebar:
    st.markdown("# 🕐 DrakkTime")
    st.divider()

    # Menu com botões GRANDES em coluna
    st.markdown("### ≡ MENU")

    if st.button("👤  Funcionários", use_container_width=True, key="btn_emp"):
        st.session_state.current_page = "👤 Funcionários"

    if st.button("⏱️  Ponto", use_container_width=True, key="btn_time"):
        st.session_state.current_page = "⏱️ Ponto"

    if st.button("📊  Resumo", use_container_width=True, key="btn_summary"):
        st.session_state.current_page = "📊 Resumo"

    # Página atual (padrão)
    if "current_page" not in st.session_state:
        st.session_state.current_page = "👤 Funcionários"

    page = st.session_state.current_page

    st.divider()

    # Stats na sidebar (maior)
    st.markdown("### 📊 Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("👥 Funcionários", len(st.session_state.employees))
    with col2:
        st.metric("📝 Registros", len(st.session_state.records))

# ===== HEADER =====
col1, col2 = st.columns([1, 10])
with col1:
    st.markdown("# 🕐")
with col2:
    st.markdown("# Sistema de Controle de Horas Extras")

st.divider()

# ===== PÁGINA: FUNCIONÁRIOS =====
if page == "👤 Funcionários":
    st.markdown("## 👤 Gerenciar Funcionários")

    # Formulário
    with st.form("form_add_employee"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Nome", placeholder="João", key="inp_fname")
            last_name = st.text_input("Sobrenome", placeholder="Silva", key="inp_lname")
        with col2:
            cpf = st.text_input("CPF", placeholder="123.456.789-00", key="inp_cpf")
            role = st.selectbox("Cargo", [r.value for r in Role], key="sel_role")

        saturday_mode = st.selectbox(
            "Modo Sábado", [s.value for s in SaturdayMode], key="sel_saturday"
        )

        submitted = st.form_submit_button("➕ Adicionar Funcionário", use_container_width=True)

        if submitted:
            if not first_name or not cpf:
                st.error("❌ Preencha nome e CPF!")
            else:
                try:
                    emp = Employee(
                        first_name=first_name,
                        last_name=last_name,
                        cpf=cpf,
                        role=Role(role),
                        registration_date=date.today().isoformat(),
                        saturday_mode=SaturdayMode(saturday_mode),
                    )
                    st.session_state.employees[emp.cpf] = emp
                    salvar_funcionarios()
                    st.success(f"✅ {emp.full_name} adicionado!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")

    st.divider()

    # Lista de funcionários
    if st.session_state.employees:
        st.markdown("### Lista de Funcionários")

        # Tabela
        emp_data = []
        for cpf, emp in st.session_state.employees.items():
            # Formatar data de cadastro
            data_cadastro = datetime.strptime(emp.registration_date, "%Y-%m-%d").strftime("%d/%m/%Y")
            emp_data.append({
                "Nome": emp.full_name,
                "CPF": emp.cpf,
                "Cargo": emp.role.value,
                "Data de Cadastro": data_cadastro,
                "Sábado": emp.saturday_mode.value,
            })

        df = pd.DataFrame(emp_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Remover
        st.markdown("### Remover Funcionário")
        emp_to_remove = st.selectbox(
            "Selecione para remover:",
            list(st.session_state.employees.keys()),
            format_func=lambda cpf: st.session_state.employees[cpf].full_name,
            key="sel_remove_emp",
        )
        if st.button("🗑️ Remover", use_container_width=True):
            emp = st.session_state.employees.pop(emp_to_remove)
            salvar_funcionarios()
            st.success(f"✅ {emp.full_name} removido!")
            st.rerun()
    else:
        st.info("📌 Nenhum funcionário adicionado ainda.")

# ===== PÁGINA: PONTO =====
elif page == "⏱️ Ponto":
    st.markdown("## ⏱️ Registrar Ponto")

    if not st.session_state.employees:
        st.warning("⚠️ Adicione funcionários primeiro!")
    else:
        with st.form("form_add_timesheet"):
            # Funcionário e Data lado a lado
            col1, col2 = st.columns([2, 1])
            with col1:
                emp_name = st.selectbox(
                    "Funcionário",
                    list(st.session_state.employees.values()),
                    format_func=lambda e: e.full_name,
                    key="sel_emp_time",
                )
            with col2:
                work_date = st.date_input("Data", value=date.today(), key="date_work")

            st.divider()

            # Tempos em coluna única, em ordem
            st.markdown("**Horários do Expediente**")
            start_time = st.time_input("Entrada", value=datetime.strptime("08:00", "%H:%M").time(), key="time_start")
            lunch_start = st.time_input("Início Almoço", value=datetime.strptime("12:00", "%H:%M").time(), key="time_lunch_start")
            lunch_end = st.time_input("Fim Almoço", value=datetime.strptime("13:00", "%H:%M").time(), key="time_lunch_end")
            end_time = st.time_input("Saída", value=datetime.strptime("17:00", "%H:%M").time(), key="time_end")

            st.divider()

            returned = st.checkbox("Retornou após expediente?", key="chk_returned")

            if returned:
                st.markdown("**Horários do Retorno**")
                extra_start = st.time_input("Retorno - Entrada", value=datetime.strptime("18:00", "%H:%M").time(), key="time_extra_start")
                extra_end = st.time_input("Retorno - Saída", value=datetime.strptime("19:00", "%H:%M").time(), key="time_extra_end")
            else:
                extra_start = None
                extra_end = None

            st.divider()

            submitted = st.form_submit_button("💾 Registrar Ponto", use_container_width=True)

            if submitted:
                try:
                    record = TimeRecord(
                        employee=emp_name,
                        work_date=work_date.isoformat(),
                        start_time=start_time.strftime("%H:%M"),
                        lunch_start=lunch_start.strftime("%H:%M"),
                        lunch_end=lunch_end.strftime("%H:%M"),
                        end_time=end_time.strftime("%H:%M"),
                        returned_after_end=returned,
                        extra_start=extra_start.strftime("%H:%M") if extra_start else None,
                        extra_end=extra_end.strftime("%H:%M") if extra_end else None,
                    )
                    st.session_state.records.append(record)
                    salvar_registros()
                    st.success("✅ Ponto registrado!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")

        st.divider()

        # Registros do dia
        if st.session_state.records:
            st.markdown("### Registros Recentes")

            record_data = []
            for rec in st.session_state.records:
                # Converter data para DD/MM/YYYY
                data_formatada = datetime.strptime(rec.work_date, "%Y-%m-%d").strftime("%d/%m/%Y")
                record_data.append({
                    "Data": data_formatada,
                    "Funcionário": rec.employee.full_name,
                    "Entrada": rec.start_time,
                    "Saída": rec.end_time,
                    "Retorno": "Sim" if rec.returned_after_end else "Não",
                })

            df_records = pd.DataFrame(record_data)
            st.dataframe(df_records, use_container_width=True, hide_index=True)

# ===== PÁGINA: RESUMO =====
elif page == "📊 Resumo":
    st.markdown("## 📊 Resumo de Horas Extras")

    if not st.session_state.records:
        st.info("📌 Nenhum registro ainda.")
    else:
        # Calcular
        summaries = summarize_overtime(st.session_state.records)

        if summaries:
            # Tabela
            summary_data = []
            total_overtime = 0
            for summary in summaries:
                hours, minutes = divmod(summary.overtime_minutes, 60)
                total_overtime += summary.overtime_minutes
                summary_data.append({
                    "Colaborador": summary.employee.full_name,
                    "CPF": summary.employee.cpf,
                    "Cargo": summary.employee.role.value,
                    "Horas Extras": f"{hours:02d}:{minutes:02d}",
                })

            st.markdown("### Horas Extras por Colaborador")
            df_summary = pd.DataFrame(summary_data)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)

            # Total
            total_hours, total_mins = divmod(total_overtime, 60)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Horas Extras", f"{total_hours:02d}:{total_mins:02d}")
            with col2:
                st.metric("Total de Minutos", f"{total_overtime}")
            with col3:
                st.metric("Funcionários", len(summaries))

            st.divider()

            # Exportar CSV
            st.markdown("### Exportar Relatório")
            csv = StringIO()
            csv.write("Colaborador,CPF,Cargo,Horas Extras\n")
            for summary in summaries:
                hours, minutes = divmod(summary.overtime_minutes, 60)
                csv.write(
                    f"{summary.employee.full_name},{summary.employee.cpf},"
                    f"{summary.employee.role.value},{hours:02d}:{minutes:02d}\n"
                )

            # Usar DD/MM/YYYY no nome do arquivo
            data_arquivo = datetime.now().strftime("%d_%m_%Y_%H%M%S")
            st.download_button(
                label="📥 Baixar CSV",
                data=csv.getvalue(),
                file_name=f"drakktime_relatorio_{data_arquivo}.csv",
                mime="text/csv",
                use_container_width=True,
            )

st.divider()
st.caption(f"v0.2.0 • {datetime.now().strftime('%d/%m/%Y %H:%M')}")
