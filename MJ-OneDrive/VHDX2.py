import subprocess
import time

def montar_vhdx(caminho_vhdx):
    script = f"""
    select vdisk file="{caminho_vhdx}"
    attach vdisk
    select partition 1
    assign letter={letra_unidade}

    """
    with open("montar_vhdx.txt", "w") as f:
        f.write(script)

    print("🔧 Montando VHDX...")
    try:
        subprocess.run(["diskpart", "/s", "montar_vhdx.txt"], check=True)
        time.sleep(3)  # Aguarda montagem
    except Exception:
        pass  # Silenciosamente ignora falhas

def desbloquear_bitlocker(letra_unidade, senha):
    print(f"🔓 Desbloqueando BitLocker na unidade {letra_unidade}...")
    comando = f"""
    Unlock-BitLocker -MountPoint '{letra_unidade}' -Password (ConvertTo-SecureString '{senha}' -AsPlainText -Force)
    """
    resultado = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)
    
    if resultado.returncode == 0:
        print("✅ BitLocker desbloqueado com sucesso.")
    else:
        print("❌ Falha ao desbloquear BitLocker.")
        print("📄 Saída do PowerShell:")
        print(resultado.stderr)

# 🔁 Fluxo principal
caminho_vhdx = r"C:\Network\OneDrive.vhdx"
letra_unidade = "Z:"
senha_bitlocker = "OneDriveMJ2025#"

montar_vhdx(caminho_vhdx)
desbloquear_bitlocker(letra_unidade, senha_bitlocker)