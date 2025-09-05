import os
import subprocess
from pathlib import Path

def reverter_protecao(path: Path, usuario="Users"):
    print(f"🔓 Revertendo proteção: {path}")

    # Restaurar herança
    subprocess.run(["icacls", str(path), "/inheritance:e"], shell=True)

    # Remover negações específicas
    subprocess.run(["icacls", str(path), "/remove:d", usuario], shell=True)

    # Remover atributos de sistema e somente leitura
    subprocess.run(["attrib", "-s", "-r", str(path)], shell=True)

def reverter_em_unidade_o():
    raiz = Path("O:/")
    if not raiz.exists():
        print("🚫 A unidade O: não está montada ou acessível.")
        return

    for item in raiz.rglob("*"):
        if item.is_dir():
            reverter_protecao(item)

    print("✅ Reversão de proteção concluída.")

if __name__ == "__main__":
    reverter_em_unidade_o()
