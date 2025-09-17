import os
import subprocess
import sys

# Função para reiniciar o script com privilégios administrativos
def run_as_admin():
    if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
        # Para versões Python >= 3.5, usa-se o 'runas'
        script = sys.argv[0]
        subprocess.run(['powershell', 'Start-Process', 'python', script, '-Verb', 'runAs'])

# Verifica se o script está sendo executado como administrador
def is_admin():
    try:
        return os.geteuid() == 0  # Funciona em sistemas Unix, mas no Windows a verificação é via subprocess.
    except AttributeError:
        return False

# Verifica se estamos executando com privilégios de administrador
if not is_admin():
    print("O script precisa de privilégios administrativos. Solicitará permissão do UAC.")
    run_as_admin()
    sys.exit(0)  # Finaliza o script para evitar que continue sem privilégios

# Nome do compartilhamento
share_name = "O$"
# Caminho da pasta a ser compartilhada
folder_path = r"D:\OneDrive"

# Verifica se a pasta existe
if not os.path.exists(folder_path):
    print("A pasta especificada não existe.")
    exit(1)

# Verifica se o compartilhamento já existe
try:
    check_command = f'net share {share_name}'
    result = subprocess.run(
        check_command,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if result.returncode == 0:
        print(f"O compartilhamento '{share_name}' já existe.")
        exit(0)
except Exception as e:
    print("Erro ao verificar o compartilhamento existente.")
    exit(1)

# Comando para criar o compartilhamento com permissão FULL para 'Todos'
share_command = f'net share {share_name}="{folder_path}" /GRANT:"Todos",FULL'

try:
    subprocess.run(
        share_command,
        shell=True,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("Compartilhamento criado com sucesso.")
except subprocess.CalledProcessError:
    print("Erro ao criar o compartilhamento. Verifique se você tem permissões de administrador.")
