import os
import sys
import ctypes
import winsound
import tempfile
import subprocess
import winreg
from PyQt6.QtWidgets import QApplication
from FunctionMessageBox import showMessageBox
from config import notificacao_sucesso, notificacao_erro1, notificacao_erro2
from SaveServer import read_server
from MapNetwork import map_drive
from Parameters import load_parameters2
from AdminUtils import is_admin, relaunch_as_admin
# Configurações
vhd_file = r"C:\Network\Network.vhdx"
icone = r"C:\Network\MJ.ico"

server_drive, label = load_parameters2()
letra_unidade = server_drive
rotulo = label
caminho = read_server()


def unidade_montada(letra):
    return os.path.exists(f"{letra}:\\")  # Verifica se a unidade está acessível

def desmontar_vhdx():
    temp = os.path.join(tempfile.gettempdir(), "unmount_vhd.txt")
    with open(temp, "w") as f:
        f.write(f"""select vdisk file="{vhd_file}"
detach vdisk
exit
""")
    try:
        subprocess.run(f'diskpart /s "{temp}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        os.remove(temp)
    except Exception:
        pass  # Silenciosamente ignora falhas

def montar_vhdx():
    if not os.path.exists(vhd_file):
        som = r"C:\MJ-Network\Resources\Sounds\error.wav"
        winsound.PlaySound(som, winsound.SND_FILENAME | winsound.SND_ASYNC)

        resposta = showMessageBox(**notificacao_erro1)
        return False

    temp = os.path.join(tempfile.gettempdir(), "mount_vhd.txt")
    with open(temp, "w") as f:
        f.write(f"""select vdisk file="{vhd_file}"
attach vdisk
select partition 1
assign letter={letra_unidade}
exit
""")

    try:
        subprocess.run(f'diskpart /s "{temp}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        os.remove(temp)
        return True
    except Exception:
        som = r"C:\MJ-Network\Resources\Sounds\error.wav"
        winsound.PlaySound(som, winsound.SND_FILENAME | winsound.SND_ASYNC)

        resposta = showMessageBox(**notificacao_erro2)
        return False

def aplicar_icone():
    try:
        key = rf"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\DriveIcons\{letra_unidade}\DefaultIcon"
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key) as reg:
            winreg.SetValueEx(reg, "", 0, winreg.REG_SZ, icone)
    except Exception:
        pass

def aplicar_label():
    try:
        ctypes.windll.kernel32.SetVolumeLabelW(f"{letra_unidade}:\\", rotulo)
    except Exception:
        pass

def desativar_autoplay():
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            winreg.SetValueEx(key, "NoDriveTypeAutoRun", 0, winreg.REG_DWORD, 0xFF)
    except Exception:
        pass  # Silenciosamente ignora falhas

def main():
    if not is_admin():
        relaunch_as_admin()
        return

    desativar_autoplay()
    map_drive(caminho, "O")

    if unidade_montada(letra_unidade):
        desmontar_vhdx()

    if not montar_vhdx():
        return

    aplicar_icone()
    aplicar_label()



    #som = os.path.abspath("Resources\\Sounds\\ready.wav")
    som = r"C:\MJ-Network\Resources\Sounds\ready.wav"
    winsound.PlaySound(som, winsound.SND_FILENAME | winsound.SND_ASYNC)


    resposta = showMessageBox(**notificacao_sucesso)
    sys.exit()

    #with open("botao.txt", "w") as f:
        #f.write(resposta.replace("&", "").lower())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
    sys.exit()
