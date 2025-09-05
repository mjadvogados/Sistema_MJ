import os
import configparser
import ctypes
from pathlib import Path
from FilesUtils import check_folder



pasta_config = Path(os.getenv("ProgramData")) / "NetworkManager"
# Cria a pasta se não existir
pasta_config.mkdir(parents=True, exist_ok=True)
# Caminho completo do arquivo .ini
arquivo_ini = folder_NetworkManager / "ConfigServer.ini"

def save_server(caminho):
    """Grava o valor da variável 'caminho' na chave 'PathServer' do arquivo INI."""
    hide_folder(pasta_config)

    config = configparser.ConfigParser()
    config.read(arquivo_ini)

    if not config.has_section("Server"):
        config.add_section("Server")

    config.set("Server", "PathServer", caminho)

    with open(arquivo_ini, "w") as configfile:
        config.write(configfile)

    #print(f"✅ Chave 'PathServer' gravada com sucesso em: {arquivo_ini}")

def read_server():
    """Lê e retorna o valor da chave 'PathServer' do arquivo INI."""
    config = configparser.ConfigParser()
    config.read(arquivo_ini)

    if config.has_section("Server") and config.has_option("Server", "PathServer"):
        path_read = config.get("Server", "PathServer")
        #print(f"📖 Valor lido da chave 'PathServer': {path_read}")
        return path_read
    else:
        #print("⚠️ Chave 'PathServer' não encontrada.")
        return None

def hide_folder(path):
    # Verifica se a pasta existe
    if os.path.exists(path):
        # Define os atributos: oculta (0x2) + sistema (0x4)
        atributos = 0x2 | 0x4
        resultado = ctypes.windll.kernel32.SetFileAttributesW(path, atributos)

        if resultado:
            return True
            #print("A pasta foi marcada como oculta e de sistema com sucesso.")
        else:
            return False
            #print("Falha ao definir os atributos da pasta.")
    else:
        return False
        #print("A pasta especificada não existe.")

def load_config():
    folder_NetworkManager = Path(os.getenv("ProgramData")) / "NetworkManager"
    # Cria a pasta se não existir
    folder_NetworkManager.mkdir(parents=True, exist_ok=True)
    # Caminho completo do arquivo .ini
    arquivo_config = folder_NetworkManager / "ConfigFolders.ini"

    if arquivo_config.exists():
        config = configparser.ConfigParser()
        config.read(arquivo_config)
        return config.get("USER", "Nome", fallback=""), config.get("PASTAS", "Selecionadas", fallback="").split(",")
    return None, []


def save_config(usuario, pastas):
    folder_NetworkManager = Path(os.getenv("ProgramData")) / "NetworkManager"
    # Cria a pasta se não existir
    folder_NetworkManager.mkdir(parents=True, exist_ok=True)
    # Caminho completo do arquivo .ini
    arquivo_config = folder_NetworkManager / "ConfigFolders.ini"

    config = configparser.ConfigParser()
    origem = r"O:"
    config["USER"] = {"Nome": usuario}
    config["PASTAS"] = {"Selecionadas": ",".join(pastas)}
    config["UNIDADE"] = {"Selecionada": "O", "Caminho": origem}
    check_folder(folder_NetworkManager)
    with open(arquivo_config, "w") as f:
        config.write(f)



"""
# Exemplo de uso
caminho = r"\\servidor\\o$"
save_server(caminho)
read_server()
"""
