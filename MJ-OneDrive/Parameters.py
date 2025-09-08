import os
from pathlib import Path
import configparser
import ast

# Caminho do arquivo de configuração
folder_NetworkManager = Path(os.getenv("ProgramData")) / "NetworkManager"
# Cria a pasta se não existir
folder_NetworkManager.mkdir(parents=True, exist_ok=True)
# Caminho completo do arquivo .ini
arquivo_config = folder_NetworkManager / "ConfigProgram.ini"

def save_parameters(
    network_drive: str,
    server_drive: str,
    source: str,
    symbolic: Path,
    junctions: Path,
    folders_ignored: set,
    label: str = 'Servidor'  # Adicionando o label como parâmetro opcional
):

    config = configparser.ConfigParser()
    
    config['Parameters'] = {
        'network_drive': network_drive,
        'server_drive': server_drive,
        'source': source,
        'symbolic': str(symbolic),
        'junctions': str(junctions),
        'folders_ignored': str(folders_ignored),
        'label': label
    }

    with open(arquivo_config, 'w') as configfile:
        config.write(configfile)

def load_parameters():
    config = configparser.ConfigParser()
    config.read(arquivo_config)

    network_drive = config.get('Parameters', 'network_drive', fallback='O:')
    server_drive = config.get('Parameters', 'server_drive', fallback='X:')
    source = config.get('Parameters', 'source', fallback=r'O:')
    symbolic = Path(config.get('Parameters', 'symbolic', fallback=r'X:\O'))
    junctions = Path(config.get('Parameters', 'junctions', fallback=r'X:'))
    label = config.get('Parameters', 'label', fallback='Servidor')

    # Interpretar string como set real
    folders_ignored_str = config.get('Parameters', 'folders_ignored', fallback='{}')
    try:
        folders_ignored = set(ast.literal_eval(folders_ignored_str))
    except (ValueError, SyntaxError):
        folders_ignored = set()

    return network_drive, server_drive, source, symbolic, junctions, label, folders_ignored

# Exemplo de uso:

if __name__ == "__main__":
    # Dados para salvar
    save_parameters(
        network_drive='O:',
        server_drive='X:',
        source=r"O:",
        symbolic=Path(r"X:\O"),
        junctions=Path(r"X:"),
        label="Servidor",
        folders_ignored={
            "Imagens", "Documentos", "90 - Compartilhado", "99 - Backup-CPJ",
            ".dropbox.cache", "Vault", "Viagem de Balão"
        }
    )

"""
    # Carregar e mostrar os dados
    network_drive, server_drive, source, symbolic, junctions, label, folders_ignored = load_parameters()
    #print("network_drive:", network_drive)
    #print("server_drive:", server_drive)
    #print("source:", source)
    #print("symbolic:", symbolic)
    #print("junctions:", junctions)
    #print("label:", label)
    #print("folders_ignored:", folders_ignored)
"""

def load_parameters2():
    config = configparser.ConfigParser()
    config.read(arquivo_config)

    network_drive = config.get('Parameters', 'network_drive', fallback='O:')
    server_drive = config.get('Parameters', 'server_drive', fallback='X:')
    label = config.get('Parameters', 'label', fallback='Servidor')
    return network_drive, server_drive, label
