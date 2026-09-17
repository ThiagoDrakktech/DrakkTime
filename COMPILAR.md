# 🚀 Como Compilar e Executar o DrakkTime

## ⚡ Opção Rápida (Recomendado)

### Passo 1: Executar os testes
Abra **PowerShell** ou **CMD** na pasta do projeto e execute:

```bash
testar.bat
```

Isso validará que tudo está funcionando corretamente.

### Passo 2: Compilar o executável
Depois execute:

```bash
compilar.bat
```

O script vai:
1. ✅ Instalar PyInstaller
2. ✅ Instalar PySimpleGUI
3. ✅ Compilar o executável
4. ✅ Abrir a pasta com o resultado

### Passo 3: Usar
Na pasta `dist/` você encontrará:
- **DrakkTime.exe** ← Execute este arquivo!

---

## 📋 Instalação Manual (Se preferir)

### 1. Instalar dependências
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Compilar
```bash
pyinstaller --onefile --windowed --name "DrakkTime" drakktime/__main__.py
```

### 3. Executável
Arquivo gerado em: `dist/DrakkTime.exe`

---

## 🎯 Resumo dos Arquivos

| Arquivo | O quê faz |
|---------|-----------|
| `testar.bat` | Valida se tudo está funcionando |
| `compilar.bat` | Gera o executável `.exe` |
| `gerar_icon.bat` | Cria um ícone customizado |
| `create_shortcut.bat` | Cria atalho no Desktop |

---

## 💡 Dicas

**Criar atalho no Desktop:**
```bash
create_shortcut.bat
```

**Executar direto sem compilar:**
```bash
python -m drakktime
```

**Testar o core sem GUI:**
```bash
python -c "from drakktime import Employee, Role; emp = Employee('João', 'Silva', '123.456.789-00', Role.GERENTE, '2024-01'); print(f'✅ {emp.full_name}')"
```

---

## ⚠️ Requisitos

- **Windows 10+**
- **Python 3.9+** (com "Add Python to PATH")
- **Conexão com internet** (primeira vez)

---

## 🆘 Troubleshooting

**"Python não encontrado"**
- Instale Python em: https://www.python.org/
- Marque "Add Python to PATH" na instalação

**"PySimpleGUI não encontrado"**
```bash
pip install PySimpleGUI --upgrade
```

**"PyInstaller não funciona"**
```bash
pip install pyinstaller --upgrade
```

---

**Pronto para começar?** Execute:
```bash
testar.bat
```

Depois:
```bash
compilar.bat
```

E aproveite seu **DrakkTime.exe**! 🎉
