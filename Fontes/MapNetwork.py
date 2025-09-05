import os
import ctypes
from FilesUtils import  run_hidden, drive_label, hide_drive 

def network_path_available(network_path):
    """
    Verifica se o caminho da rede está disponível.
    """
    try:
        return os.path.exists(network_path)
    except Exception:
        return False

def show_notification(message, title="Aviso"):
    # Exibe uma notificação com MessageBox padrão do Windows.
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x30)  # 0x30 = MB_ICONWARNING

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
    # Verifica se o caminho da rede está acessível
    #if not network_path_available(network_path):
    #show_notification(f"Não foi possível acessar o caminho da rede:\n{network_path}\n\nVerifique a conexão ou escolha outro servidor.")
    #return  # Volta para a janela de seleção do servidor (comportamento externo esperado)

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

drive_label("O:", "Backups")