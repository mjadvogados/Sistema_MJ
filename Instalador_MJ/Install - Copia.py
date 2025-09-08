import os
import zipfile
import ctypes
import shutil
import subprocess
import winshell
from win32com.client import Dispatch

# Caminhos
base_dir = os.path.abspath(os.path.dirname(__file__))
resources_dir = os.path.join(base_dir, 'Resources')
network_zip = os.path.join(resources_dir, 'network.zip')
mj_network_zip = os.path.join(resources_dir, 'MJ-Network.zip')
vhdxrun_zip = os.path.join(resources_dir, 'VHDXRun.zip')

# Destinos
network_dest = r'C:\Network'
mj_network_dest = r'C:\MJ-Network'
vhdxrun_dest = r'C:\Windows\MJ'

# Função para extrair ZIP
def extract_zip(zip_path, dest_path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_path)

# Função para definir atributos de pasta (oculta + sistema)
def set_folder_attributes_hidden_system(folder_path):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    FILE_ATTRIBUTE_SYSTEM = 0x04
    attributes = FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM
    ctypes.windll.kernel32.SetFileAttributesW(folder_path, attributes)

# Função para criar atalho
def create_shortcut(target, shortcut_path, working_dir=None):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = working_dir or os.path.dirname(target)
    shortcut.IconLocation = target
    shortcut.save()

# Função para criar a tarefa agendada
def create_scheduled_task(task_name, executable_path):
    # Verifica se a tarefa já existe
    check_cmd = ['schtasks', '/Query', '/TN', task_name]
    task_exists = subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

    # Remove se já existir
    if task_exists:
        delete_cmd = ['schtasks', '/Delete', '/TN', task_name, '/F']
        subprocess.run(delete_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Cria a nova tarefa
    create_cmd = [
        'schtasks', '/Create',
        '/SC', 'ONLOGON',
        '/RL', 'HIGHEST',
        '/TN', task_name,
        '/TR', f'"{executable_path}"',
        '/F'
    ]
    subprocess.run(create_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 1. Extrair os arquivos ZIP
extract_zip(network_zip, network_dest)
extract_zip(mj_network_zip, mj_network_dest)
extract_zip(vhdxrun_zip, vhdxrun_dest)

# 2. Definir atributos das pastas
set_folder_attributes_hidden_system(network_dest)
set_folder_attributes_hidden_system(vhdxrun_dest)
set_folder_attributes_hidden_system(mj_network_dest)

# 3. Criar atalhos no Desktop
desktop = winshell.desktop()
vhdx_exe = os.path.join(vhdxrun_dest, 'VHDXRun.exe')
network_setup_exe = os.path.join(mj_network_dest, 'NetworkSetup.exe')

create_shortcut(vhdx_exe, os.path.join(desktop, 'Servidor - Conectar.lnk'))
create_shortcut(network_setup_exe, os.path.join(desktop, 'Servidor - Configuração.lnk'))

# 4. Criar tarefa agendada
create_scheduled_task("WinShell Update", vhdx_exe)
