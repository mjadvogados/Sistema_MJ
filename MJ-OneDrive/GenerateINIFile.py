import os

# Caminho do arquivo
caminho_arquivo = r"C:\ProgramDataNetworkManager\OneDriveConfig.ini"

# Conteúdo padrão do arquivo INI
conteudo_ini = """[Paths]
origem = P:\
destino_simbolico = Z:\\O\\
destino_juncoes = Z:\\

[Config]
label = OneDrive_Offline
"""

# Verifica se o arquivo já existe
if not os.path.exists(caminho_arquivo):
    # Garante que o diretório existe
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    # Cria o arquivo com o conteúdo especificado
    with open(caminho_arquivo, 'w') as arquivo:
        arquivo.write(conteudo_ini)
    print("Arquivo criado com sucesso.")
else:
    print("O arquivo já existe.")
