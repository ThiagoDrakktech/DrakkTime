# 📦 Compilação do DrakkTime para EXE

## ✅ Como Compilar

### Passo 1: Execute o compilador
Clique 2x em: **`COMPILAR_EXE.bat`**

Vai:
1. ✅ Instalar PyInstaller
2. ✅ Compilar o código
3. ✅ Gerar `dist/DrakkTime.exe`

(Leva 2-3 minutos)

### Passo 2: Teste
Clique 2x em: **`dist/DrakkTime.exe`**

Deve abrir normalmente no navegador!

---

## 🚀 Como Usar no PC do Trabalho

### Método 1: Copiar Pasta (Recomendado)
1. Copie a pasta **`dist`** inteira
2. Cole no PC do trabalho em qualquer lugar
3. Clique 2x em **`DrakkTime.exe`**
4. Pronto! Funciona sem instalação

### Método 2: Só o EXE
1. Se quiser apenas o .exe sem arquivos extras
2. Use: **`dist/DrakkTime.exe` (sem outras dependências)**

---

## 💾 Dados

Os dados são salvos em:
```
.drakktime_data/
├── employees.json
└── records.json
```

**Criada automaticamente** ao rodar o programa pela primeira vez

---

## ⚙️ Requisitos no PC do Trabalho

- Windows 10+
- **Nenhuma instalação de Python necessária!**
- Só precisa clicar 2x no `.exe`

---

## 📊 Resumo

| Item | Detalhes |
|------|----------|
| Arquivo | `dist/DrakkTime.exe` |
| Tamanho | ~150-200 MB |
| Requisitos | Windows 10+ |
| Instalação | Nenhuma - é portável! |
| Dados | Salvos em `.drakktime_data/` |

---

## 🆘 Se der erro

Se aparecer erro ao compilar, tente:
```bash
Feche tudo e execute de novo: COMPILAR_EXE.bat
```

Se continuar, pode ser que o PyInstaller não gostou da estrutura. Nesse caso:
```bash
Rode direto com o Streamlit:
EXECUTAR_STREAMLIT.bat
```

---

**Pronto para instalar!** 🎉
