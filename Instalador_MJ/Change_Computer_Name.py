import socket
import subprocess
import sys
import ctypes

# Lista de nomes permitidos
nomes_permitidos = []

# Pelotas-01 até Pelotas-15
nomes_permitidos += [f"Pelotas-{i:02}" for i in range(1, 16)]

# RG-01 até RG-15
nomes_permitidos += [f"RG-{i:02}" for i in range(1, 16)]

# SVP-01 até SVP-08
nomes_permitidos += [f"SVP-{i:02}" for i in range(1, 9)]

# Nomes fixos
nomes_permitidos += [
    "iMac", "iMac1", "iMac2",
    "Graciele-Acer", "Graciele-Dell",
    "Servidor", "Servidor-RG", "Servidor-Pel", "Servidor-SVP"
]

# Prefixo base para novos nomes
NOME_BASE = "MJ"

# Verifica se está sendo executado como administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Testa se um nome está em uso na rede local
def nome_em_uso(nome):
    try:
        subprocess.check_output(
            ["ping", "-n", "1", "-w", "500", nome],
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True  # Ping bem-sucedido
    except subprocess.CalledProcessError:
        return False  # Falha no ping (nome não encontrado)

# Gera um nome disponível na rede (ex: MJ-01, MJ-02, etc)
def gerar_nome_disponivel():
    for i in range(1, 100):  # até MJ-99
        nome_teste = f"{NOME_BASE}-{i:02}"
        if not nome_em_uso(nome_teste):
            return nome_teste
    return None  # Nenhum nome disponível

# Renomeia o computador de forma silenciosa
def mudar_nome_computador(novo_nome):
    subprocess.run(
        ["wmic", "computersystem", "where", "name='%COMPUTERNAME%'", "call", "rename", novo_nome],
        creationflags=subprocess.CREATE_NO_WINDOW,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def main():
    if not is_admin():
        sys.exit(0)

    nome_atual = socket.gethostname()

    if nome_atual not in nomes_permitidos:
        novo_nome = gerar_nome_disponivel()
        if novo_nome:
            mudar_nome_computador(novo_nome)

if __name__ == "__main__":
    main()
