"""Ponto de entrada do DrakkTime."""

import sys
import os

# Desabilitar hot reload e behaviors problemáticos
os.environ["STREAMLIT_CLIENT_SHOWERRORDETAILS"] = "false"
os.environ["STREAMLIT_LOGGER_LEVEL"] = "error"
os.environ["STREAMLIT_SERVER_RUNONSAVE"] = "false"
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

if __name__ == "__main__":
    try:
        import streamlit.cli as stcli

        # Encontrar o arquivo do app
        app_path = os.path.join(os.path.dirname(__file__), "ui", "streamlit_app.py")

        # Rodar Streamlit COM CONTROLE DE ENCERRAMENTO
        sys.argv = ["streamlit", "run", app_path, "--logger.level=error"]
        stcli.main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)
    finally:
        sys.exit(0)




