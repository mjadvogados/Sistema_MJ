import os
import shutil
import subprocess
from pathlib import Path
import winreg

def remover_pasta(pasta):
    if pasta.exists() and pasta.is_dir():
        try:
            shutil.rmtree(pasta)
            print(f"Pasta removida: {pasta}")
        except Exception as e:
            print(f"Erro ao remover {pasta}: {e}")

def desmontar_unidade_x():
    try:
        resultado = subprocess.run(["subst"], capture_output=True, text=True)
        if "X:\\" in resultado.stdout:
            subprocess.run(["subst", "X:", "/d"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Unidade X: desmontada.")
    except Exception as e:
        print(f"Erro ao desmontar X:: {e}")

def remover_dropbox_usuarios():
    base_users = Path("C:/Users")
    if base_users.exists():
        for usuario in base_users.iterdir():
            dropbox_path = usuario / "Dropbox"
            remover_pasta(dropbox_path)

def remover_dropbox_mj():
    pasta = Path("C:/MJ-Servidor/MJ1/Dropbox")
    remover_pasta(pasta)

def desinstalar_dropbox():
    try:
        # Verifica no registro se Dropbox está instalado
        chave = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        for root in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            try:
                with winreg.OpenKey(root, chave) as hkey:
                    for i in range(0, winreg.QueryInfoKey(hkey)[0]):
                        subkey_name = winreg.EnumKey(hkey, i)
                        with winreg.OpenKey(hkey, subkey_name) as subkey:
                            try:
                                nome = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if "Dropbox" in nome:
                                    uninstall_str = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                    
                                    # Remove aspas extras e adiciona silencioso
                                    if uninstall_str.startswith('"') and uninstall_str.endswith('"'):
                                        uninstall_str = uninstall_str[1:-1]
                                    
                                    cmd = [uninstall_str, "/S"]
                                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False)
                                    print("Dropbox desinstalado.")
                                    return
                            except FileNotFoundError:
                                continue
            except FileNotFoundError:
                continue
    except Exception as e:
        print(f"Erro ao tentar desinstalar Dropbox: {e}")

def main():
    desinstalar_dropbox()
    desmontar_unidade_x()
    remover_dropbox_usuarios()
    remover_dropbox_mj()

if __name__ == "__main__":
    main()
