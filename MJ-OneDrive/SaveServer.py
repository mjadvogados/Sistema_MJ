import os
import configparser
import ctypes
from pathlib import Path



#from FilesUtils import check_folder  # Verifique se esse módulo está acessível

# Caminho da pasta onde ficarão os arquivos de configuração
pasta_config = Path(os.getenv("ProgramData")) / "NetworkManager"
# Cria a pasta se não existir
pasta_config.mkdir(parents=True, exist_ok=True)
# Caminho completo do arquivo .ini principal
arquivo_ini = pasta_config / "ConfigServer.ini"

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

def read_server():
    """Lê e retorna o valor da chave 'PathServer' do arquivo INI."""
    config = configparser.ConfigParser()
    config.read(arquivo_ini)

    if config.has_section("Server") and config.has_option("Server", "PathServer"):
        return config.get("Server", "PathServer")
    else:
        return None

def hide_folder(path):
    """Define a pasta como oculta e de sistema no Windows."""
    if os.path.exists(path):
        atributos = 0x2 | 0x4  # Oculta + Sistema
        resultado = ctypes.windll.kernel32.SetFileAttributesW(str(path), atributos)
        return resultado != 0
    return False

def load_config2():
    """Carrega o nome do usuário e pastas selecionadas a partir do arquivo INI."""
    arquivo_config = pasta_config / "ConfigFolders.ini"

    if arquivo_config.exists():
        config = configparser.ConfigParser()
        config.read(arquivo_config)
        nome_usuario = config.get("USER", "Nome", fallback="")
        pastas = config.get("PASTAS", "Selecionadas", fallback="").split(",")
        return nome_usuario, pastas
    return None, []


def load_config():
    """Carrega as pastas selecionadas do usuário logado a partir do arquivo INI."""
    pasta_config = Path(r"C:\ProgramData\NetworkManager")
    arquivo_config = pasta_config / "ConfigFolders.ini"

    if arquivo_config.exists():
        usuario_logado = os.getlogin().strip()
        config = configparser.ConfigParser()
        config.read(arquivo_config)

        if usuario_logado in config:
            pastas = config.get(usuario_logado, "selecionadas", fallback="").split(",")
            pastas = [p.strip() for p in pastas if p.strip()]
            return usuario_logado, pastas
        else:
            print(f"⚠️ Usuário '{usuario_logado}' não encontrado no arquivo de configuração.")
            return usuario_logado, []
    else:
        print("⚠️ Arquivo de configuração não encontrado.")
        return None, []



def save_config2(usuario, pastas):
    """Salva o nome do usuário, pastas selecionadas e unidade no arquivo INI."""
    arquivo_config = pasta_config / "ConfigFolders.ini"

    config = configparser.ConfigParser()
    origem = r"O:"
    config["USER"] = {"Nome": usuario}
    config["PASTAS"] = {"Selecionadas": ",".join(pastas)}
    config["UNIDADE"] = {"Selecionada": "O", "Caminho": origem}

    check_folder(pasta_config)

    with open(arquivo_config, "w") as f:
        config.write(f)


def check_folder(path):
    """Cria a pasta se não existir."""
    Path(path).mkdir(parents=True, exist_ok=True)

def save_config(usuario, pastas):
    """Salva ou atualiza as pastas selecionadas por um usuário no arquivo INI."""
    pasta_config = Path(r"C:\ProgramData\NetworkManager")
    arquivo_config = pasta_config / "ConfigFolders.ini"

    check_folder(pasta_config)

    config = configparser.ConfigParser()

    # Lê o arquivo existente, se houver
    if arquivo_config.exists():
        config.read(arquivo_config)

    # Atualiza ou cria a seção do usuário
    config[usuario] = {
        "selecionadas": ",".join(pastas)
    }

    # Salva de volta o arquivo completo com as mudanças
    with open(arquivo_config, "w") as f:
        config.write(f)

    #print(f"✅ Configuração salva para o usuário '{usuario}' com {len(pastas)} pastas.")







# Exemplo de uso:
# caminho = r"\\servidor\\o$"
# save_server(caminho)
# print(read_server())
