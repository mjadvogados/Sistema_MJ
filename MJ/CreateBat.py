import os

def create_bat(server):
    # Garante que a pasta C:\MJ-Network exista
    pasta_destino = r"C:\MJ-Network"
    os.makedirs(pasta_destino, exist_ok=True)

    # Caminho completo do arquivo
    caminho_arquivo = os.path.join(pasta_destino, "MJ.bat")

    # Conteúdo do arquivo BAT
    conteudo = f"""@echo off
net use O: /delete /yes
net use O: {server} /user:administrador mj2145mj /persistent:yes
exit
"""

    # Escreve o conteúdo no arquivo
    with open(caminho_arquivo, "w") as arquivo:
        arquivo.write(conteudo)

    print(f"Arquivo MJ.bat criado em: {caminho_arquivo}")

# Exemplo de uso:
#servidor_input = r"\\servidor-svp\o$"
#create_bat(servidor_input)
