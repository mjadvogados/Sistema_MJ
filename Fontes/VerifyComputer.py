import socket
import sys

# Caminho do arquivo com a lista de computadores permitidos
CAMINHO_ARQUIVO = "computadores_permitidos.txt"

def obter_nome_computador():
    return socket.gethostname()

def verificar_autorizacao(nome_computador, caminho_arquivo):
    try:
        with open(caminho_arquivo, "r") as arquivo:
            computadores_permitidos = [linha.strip() for linha in arquivo.readlines()]
            return nome_computador in computadores_permitidos
    except FileNotFoundError:
        print(f"Arquivo '{caminho_arquivo}' não encontrado.")
        sys.exit(1)

def main():
    nome_computador = obter_nome_computador()
    if not verificar_autorizacao(nome_computador, CAMINHO_ARQUIVO):
        print(f"Computador '{nome_computador}' não está autorizado. Encerrando o programa.")
        sys.exit(1)
    else:
        print(f"Computador '{nome_computador}' autorizado. Continuando a execução...")

if __name__ == "__main__":
    main()
