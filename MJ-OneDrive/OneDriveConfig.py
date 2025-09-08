import sys
import configparser
from pathlib import Path

INI_PATH = Path(r"C:\ProgramData\NetworkManager\OneDriveConfig.ini")

def salvar_config(origem, destino_simbolico, destino_juncoes, label, pastas_ignoradas):
    config = configparser.ConfigParser()

    config['Paths'] = {
        'origem': str(origem),
        'destino_simbolico': str(destino_simbolico),
        'destino_juncoes': str(destino_juncoes)
    }

    config['Config'] = {
        'label': label,
        'pastas_ignoradas': ','.join(pastas_ignoradas)
    }

    INI_PATH.parent.mkdir(parents=True, exist_ok=True)
    with INI_PATH.open('w') as configfile:
        config.write(configfile)

def carregar_config():
    config = configparser.ConfigParser()
    config.read(INI_PATH)

    origem = Path(config.get('Paths', 'origem', fallback=r"P:\\"))
    destino_simbolico = Path(config.get('Paths', 'destino_simbolico', fallback=r"Z:\\O\\"))
    destino_juncoes = Path(config.get('Paths', 'destino_juncoes', fallback=r"Z:\\"))
    label = config.get('Config', 'label', fallback="OneDrive_Online")
    caminho_vhdx = config.get("Paths", "caminhovhdx", fallback=r"C:\\Network\\OneDrive.vhdx")
    caminho_icone = config.get("Config", "icone", fallback=r"C:\Network\OneDrive.ico")
    #ignoradas = config.get('Config', 'pastas_ignoradas', fallback="").split(',')

    #ignoradas = [p.strip() for p in ignoradas if p.strip()]
    return origem, destino_simbolico, destino_juncoes, label, caminho_vhdx, caminho_icone


