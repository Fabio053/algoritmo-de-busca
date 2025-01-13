import os
import sys
import subprocess
import platform

def get_virtualenv_path():
    if getattr(sys, 'frozen', False):
        # Quando o código está rodando como executável
        return os.path.join(sys._MEIPASS, ".venv")
    else:
        # Quando o código está rodando no ambiente de desenvolvimento
        return os.path.join(os.path.dirname(__file__), ".venv")

def run_with_virtualenv():
    venv_path = get_virtualenv_path()
    
    # Determinando o comando de ativação do ambiente virtual conforme o sistema operacional
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_path, "Scripts", "activate")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")
    
    # Comando para ativar o ambiente virtual e rodar o script
    command = f"{activate_script} && python busca-selenium.py"
    
    # Rodar o comando
    subprocess.run(command, shell=True)

def run_streamlit_app():
    script_path = os.path.join(os.path.dirname(__file__), "busca-selenium.py")
    subprocess.run(["streamlit", "run", script_path])

if __name__ == "__main__":
    run_with_virtualenv()
    run_streamlit_app()
