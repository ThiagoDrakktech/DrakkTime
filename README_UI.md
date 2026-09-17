# 🕐 DrakkTime - Sistema de Controle de Horas Extras

Uma aplicação simples e eficiente para controlar e calcular horas extras de funcionários, desenvolvida para Windows 10+.

## 🎯 Funcionalidades

- ✅ **Gerenciamento de Funcionários**: Adicione e gerencie dados de funcionários com diferentes cargos
- ✅ **Registro de Ponto**: Registre entrada, saída, intervalos e retornos pós-expediente
- ✅ **Cálculo Automático**: Calcula automaticamente horas extras baseado em regras de negócio
- ✅ **Resumo de Horas**: Visualize um resumo consolidado de horas extras por funcionário
- ✅ **Exportar para CSV**: Exporte relatórios em formato CSV

## 🚀 Instalação

### 1. Clonar o repositório
```bash
git clone <seu-repo>
cd DrakkTime
```

### 2. Criar ambiente virtual (recomendado)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

## 💻 Como Usar

### Executar a aplicação:
```bash
python -m drakktime
```

Ou diretamente:
```bash
python drakktime/ui/main_window.py
```

### Passos básicos:

1. **Adicione Funcionários** (Aba 👤 Funcionários)
   - Preencha dados: Nome, Sobrenome, CPF, Cargo
   - Configure modo de sábado (alternado ou todo sábado)
   - Clique em "➕ Adicionar Funcionário"

2. **Registre Pontos** (Aba ⏱️ Ponto)
   - Selecione o funcionário
   - Digite horários de entrada, almoço e saída
   - Se houve retorno após expediente, marque a opção
   - Clique em "💾 Registrar Ponto"

3. **Visualize Resumo** (Aba 📊 Resumo)
   - Clique em "🔄 Atualizar" para calcular horas extras
   - Exporte em CSV se necessário

## 📊 Estrutura de Cargos

- **Gerente**: 8h/dia (exceto sábado e domingo)
- **Assistente Administrativo**: 8h/dia (exceto sábado e domingo)
- **Oficial de Manutenção**: 12h/dia
- **Auxiliar de Manutenção**: 8h/dia (exceto sábado e domingo)

## 🔄 Modo Sábado

- **Alternado**: Funciona 8h + 48 min em dias úteis, não trabalha sábados alternados
- **Todo Sábado**: Funciona 8h em dias úteis + 4h aos sábados

## 📁 Estrutura do Projeto

```
drakktime/
├── core/              # Lógica de negócio
│   ├── models.py      # Dataclasses
│   ├── calculator.py  # Cálculos
│   ├── formatter.py   # Formatação
│   └── utils.py       # Utilitários
├── ui/                # Interface gráfica
│   ├── main_window.py # Janela principal
│   ├── styles.py      # Temas
│   └── forms.py       # Formulários
├── config/            # Configurações
└── assets/            # Recursos (ícones, etc)
```

## 🛠️ Desenvolvimento

### Dependências:
- Python 3.9+
- PySimpleGUI 4.60.0+

### Rodar testes:
```bash
python -m pytest
```

## 📝 Licença

MIT

## 👨‍💻 Autor

DrakkTime - 2024
