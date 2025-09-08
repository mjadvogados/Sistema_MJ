import sys
import subprocess
import time
import os
import tempfile
import winreg
import ctypes
from OneDriveConfig import carregar_config
from SetVolumeLabel import change_label
from ApplyJunctions import  apply_junctions
#Carregando informações do arquivo OneDriveConfig.ini
origem, destino_simbolico, destino_juncoes, label, caminho_vhdx, caminho_icone = carregar_config()
# Excluindo variáveis desnecessárias
del origem, destino_simbolico

# Definindo as variáveis
#caminho_vhdx = r"C:\Network\OneDrive.vhdx"
caminho_vhdx = caminho_vhdx
icone = caminho_icone
#icone = r"C:\Network\OneDrive.ico"
letra_unidade = str(destino_juncoes).rstrip("\\")
senha_bitlocker = "OneDriveMJ2025#"
rotulo = label

def unidade_montada(letra_unidade):
    return os.path.exists(f"{letra_unidade}\\")

def vhdx_esta_anexado(caminho_vhdx):
    comando = f"""
    list vdisk
    """
    resultado = subprocess.run(["diskpart"], input=comando, text=True, capture_output=True)
    return caminho_vhdx.lower() in resultado.stdout.lower()

def desmontar_vhdx(caminho_vhdx, letra_unidade):
    script = f"""
    select vdisk file="{caminho_vhdx}"
    detach vdisk
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_script:
        temp_script.write(script)
        temp_script_path = temp_script.name

    print(f"🧹 Desmontando VHDX...")
    subprocess.run(["diskpart", "/s", temp_script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    os.remove(temp_script_path)

def montar_vhdx(caminho_vhdx, letra_unidade):
    if vhdx_esta_anexado(caminho_vhdx):
        desmontar_vhdx(caminho_vhdx, letra_unidade)

    script = f"""
    select vdisk file="{caminho_vhdx}"
    attach vdisk
    select partition 1
    assign letter={letra_unidade}
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_script:
        temp_script.write(script)
        temp_script_path = temp_script.name

    print("🔧 Montando VHDX...")
    subprocess.run(["diskpart", "/s", temp_script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)

    os.remove(temp_script_path)

def desbloquear_bitlocker(letra_unidade, senha):
    print(f"🔓 Desbloqueando BitLocker na unidade {letra_unidade}...")
    comando = (
        f"Unlock-BitLocker -MountPoint '{letra_unidade}' "
        f"-Password (ConvertTo-SecureString '{senha}' -AsPlainText -Force)"
    )
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", comando],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def aplicar_icone():
    try:
        key = rf"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\DriveIcons\{letra_unidade}\DefaultIcon"
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key) as reg:
            winreg.SetValueEx(reg, "", 0, winreg.REG_SZ, icone)
    except Exception:
        pass

def aplicar_rotulo():
    try:
        ctypes.windll.kernel32.SetVolumeLabelW(f"{letra_unidade}:\\", rotulo)
    except Exception:
        pass


# 🔁 Fluxo principal

montar_vhdx(caminho_vhdx, letra_unidade)
desbloquear_bitlocker(letra_unidade, senha_bitlocker)
time.sleep(5)
aplicar_icone()
apply_junctions()
change_label(letra_unidade, rotulo)
