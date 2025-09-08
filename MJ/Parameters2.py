import os
from pathlib import Path
import configparser
import ast

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
    #source = Path(config.get('Parameters', 'source', fallback=r'O:\')).resolve()
    source = config.get('Parameters', 'source', fallback=r'O:')
    symbolic = Path(config.get('Parameters', 'symbolic', fallback=r'X:\O')).resolve()
    junctions = Path(config.get('Parameters', 'junctions', fallback=r'X:\')).resolve()
    label = config.get('Parameters', 'label', fallback='Servidor')

    # Interpreta a string como set
    folders_ignored_str = config.get('Parameters', 'folders_ignored', fallback='set()')
    try:
        folders_ignored = set(ast.literal_eval(folders_ignored_str))
    except (ValueError, SyntaxError):
        folders_ignored = set()

    return network_drive, server_drive, source, symbolic, junctions, label, folders_ignored



def load_parameters2():
    config = configparser.ConfigParser()
    config.read(arquivo_config)

    network_drive = config.get('Parameters', 'network_drive', fallback='O:')
    server_drive = config.get('Parameters', 'server_drive', fallback='X:')
    label = config.get('Parameters', 'label', fallback='Servidor')
    return network_drive, server_drive, label
