import requests
import os
import sys
import shutil
import subprocess
import time

VERSAO_ATUAL = "1.0.0"
URL_VERSION = "https://meusite.com/atualizador/version.json"
NOME_EXE = "meu_programa.exe"
NOME_EXE_NOVO = "meu_programa_novo.exe"

def obter_versao_online():
    try:
        response = requests.get(URL_VERSION)
        if response.status_code == 200:
            dados = response.json()
            return dados["version"], dados["url"]
    except Exception as e:
        print(f"Erro ao verificar versão online: {e}")
    return None, None

def comparar_versoes(v1, v2):
    return tuple(map(int, v1.split("."))) < tuple(map(int, v2.split(".")))

def baixar_nova_versao(url):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(NOME_EXE_NOVO, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("Download concluído.")
        return True
    except Exception as e:
        print(f"Erro no download: {e}")
        return False

def substituir_e_reiniciar():
    print("Aguardando finalização do processo atual...")
    time.sleep(2)

    atual = sys.executable
    os.rename(atual, atual + ".old")
    os.rename(NOME_EXE_NOVO, atual)

    subprocess.Popen([atual])
    sys.exit()

def verificar_e_atualizar():
    versao_online, url_download = obter_versao_online()
    if not versao_online:
        print("Não foi possível obter a versão online.")
        return

    if comparar_versoes(VERSAO_ATUAL, versao_online):
        print(f"Nova versão disponível: {versao_online}")
        if baixar_nova_versao(url_download):
            substituir_e_reiniciar()
    else:
        print("Você já está usando a versão mais recente.")

if __name__ == "__main__":
    verificar_e_atualizar()
    # Aqui segue o resto do seu programa normalmente
    print("Executando o programa principal...")
    # ... seu código ...
