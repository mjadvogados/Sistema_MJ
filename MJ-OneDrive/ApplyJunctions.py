import os
import getpass
import re
from pathlib import Path
from FilesUtils import set_attrib, run_hidden, clear_target
from SaveServer import load_config
from OneDriveConfig import carregar_config
from Parameters import load_parameters

# Carregar parâmetros do arquivo .ini
network_drive, server_drive, source, symbolic, junctions, label, folders_ignored = load_parameters()
pastas_ignoradas = folders_ignored
# Excluindo as variáveis desnecessárias
del network_drive, server_drive, source, symbolic, junctions, label

#Carregando informações do arquivo OneDriveConfig.ini
origem, destino_simbolico, destino_juncoes, label, caminho_vhdx, caminho_icone = carregar_config()

# Caminhos convertidos para Path
#origem = Path(r"P:\\")
#destino_simbolico = Path(r"Z:\\O\\")
#destino_juncoes = Path(r"Z:\\")
#labelX = "OneDrive_Online"



def criar_juncoes(pastas):
    destino_simbolico.mkdir(parents=True, exist_ok=True)
    contador_sem_numero = 71
    padrao_numero = re.compile(r'^(\d{2})')

    for pasta in pastas:
        if pasta in pastas_ignoradas:
            continue

        caminho_origem = origem / pasta
        if not caminho_origem.is_dir():
            continue

        match = padrao_numero.match(pasta)
        if match:
            nome_link = match.group(1)
        else:
            if contador_sem_numero > 89:
                print('❌ Número máximo de pastas sem numeração excedido. Operação cancelada.')
                return
            nome_link = f'{contador_sem_numero:02d}'
            contador_sem_numero += 1

        link = destino_simbolico / nome_link
        juncao = destino_juncoes / pasta

        run_hidden(f'mklink /D "{link}" "{caminho_origem}"')
        run_hidden(f'mklink /J "{juncao}" "{link}"')

    set_attrib(destino_simbolico)

def apply_junctions():
    usuario_logado = getpass.getuser()

    usuario, selecionadas = load_config()

    if usuario != usuario_logado:
        print("⚠️ Nenhuma configuração encontrada para o usuário atual.")
        return

    if not selecionadas:
        print("⚠️ Nenhuma pasta selecionada para este usuário.")
        return

    clear_target(destino_simbolico, destino_juncoes)
    criar_juncoes(selecionadas)

    # save_config(usuario_logado, selecionadas)
    # openX()
    # print("✅ Junções aplicadas com sucesso e unidade X: aberta!")

if __name__ == "__main__":
    apply_junctions()
