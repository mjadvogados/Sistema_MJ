import os
import shutil
import subprocess
from pathlib import Path

def remover_pasta(pasta):
    if pasta.exists() and pasta.is_dir():
        try:
            shutil.rmtree(pasta)
            print(f"Pasta removida: {pasta}")
        except Exception as e:
            print(f"Erro ao remover {pasta}: {e}")

def desmontar_unidade_x():
    try:
        # Verifica se X: está montada como subst
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

def main():
    desmontar_unidade_x()
    remover_dropbox_usuarios()
    remover_dropbox_mj()

if __name__ == "__main__":
    main()
