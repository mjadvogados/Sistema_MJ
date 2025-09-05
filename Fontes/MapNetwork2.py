import subprocess
import win32com.client
import winreg

def run_hidden(cmd):
    subprocess.run(cmd, shell=True, creationflags=0x08000000)  # CREATE_NO_WINDOW

def drive_label(drive_letter, label):
    shell = win32com.client.Dispatch("Shell.Application")
    shell.NameSpace(drive_letter).Self.Name = label


def hide_drive(letter):
    """
    Oculta uma unidade de disco no Windows modificando a chave de registro NoDrives.

    Parâmetro:
    - letter: Letra da unidade a ser ocultada (ex: 'O')
    """
    letter = letter.upper()
    posicao = ord(letter) - ord('A')
    bitmask = 1 << posicao  # Cria máscara binária para a letra

    chave_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"

    try:
        # Tenta abrir a chave com permissões de leitura e escrita
        chave = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            chave_path,
            0,
            winreg.KEY_READ | winreg.KEY_SET_VALUE
        )
    except FileNotFoundError:
        # Se a chave não existir, cria com permissões de escrita
        chave = winreg.CreateKey(
            winreg.HKEY_LOCAL_MACHINE,
            chave_path
        )
        valor_atual = 0
    else:
        try:
            # Tenta ler o valor atual de NoDrives
            valor_atual, _ = winreg.QueryValueEx(chave, "NoDrives")
        except FileNotFoundError:
            valor_atual = 0

    # Atualiza o valor combinando com a nova máscara
    novo_valor = valor_atual | bitmask

    try:
        winreg.SetValueEx(chave, "NoDrives", 0, winreg.REG_DWORD, novo_valor)
    except PermissionError:
        print("❌ Permissão negada ao tentar modificar NoDrives. Execute como administrador.")
    finally:
        winreg.CloseKey(chave)

def map_drive(network_path, drive_letter, username="administrador", password="mj2145mj", label="Servidor"):
    """
    Mapeia e oculta uma unidade de rede no Windows.
    
    Parâmetros:
    - network_path: Caminho da rede
    - drive_letter: Letra da unidade
    - username: Usuário para autenticação
    - password: Senha para autenticação
    - label: Nome que aparecerá como rótulo da unidade
    """
    # Remove conexões anteriores
    run_hidden('net use * /delete /yes')
    run_hidden(f'net use {drive_letter}: /delete /yes')

    # Mapeia unidade
    cmd_map = f'net use {drive_letter}: {network_path} /user:{username} {password} /persistent:yes'
    run_hidden(cmd_map)

    # Define rótulo
    drive_label(f"{drive_letter}:\\", label)

    # Oculta unidade
    hide_drive(drive_letter)

"""
Como importar e como chamar a função:
from Map_Network import map_drive

# Exemplo de chamada
map_drive(r"\\servidor\\O$", "O")

"""