import subprocess
import time
import os

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
    with open("desmontar_vhdx.txt", "w") as f:
        f.write(script)

    print(f"🧹 Desmontando VHDX...")
    subprocess.run(["diskpart", "/s", "desmontar_vhdx.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

def montar_vhdx(caminho_vhdx, letra_unidade):
    if vhdx_esta_anexado(caminho_vhdx):
        desmontar_vhdx(caminho_vhdx, letra_unidade)

    script = f"""
    select vdisk file="{caminho_vhdx}"
    attach vdisk
    select partition 1
    assign letter={letra_unidade}
    """
    with open("montar_vhdx.txt", "w") as f:
        f.write(script)

    print("🔧 Montando VHDX...")
    subprocess.run(["diskpart", "/s", "montar_vhdx.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)


def desbloquear_bitlocker(letra_unidade, senha):
    print(f"🔓 Desbloqueando BitLocker na unidade {letra_unidade}...")
    comando = (
        f"Unlock-BitLocker -MountPoint '{letra_unidade}' "
        f"-Password (ConvertTo-SecureString '{senha}' -AsPlainText -Force)"
    )
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", comando],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 🔁 Fluxo principal
caminho_vhdx = r"C:\Network\OneDrive.vhdx"
letra_unidade = "Z:"
senha_bitlocker = "OneDriveMJ2025#"

montar_vhdx(caminho_vhdx, letra_unidade)
desbloquear_bitlocker(letra_unidade, senha_bitlocker)
