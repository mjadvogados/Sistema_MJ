import os
import getpass
import re
from pathlib import Path
from FilesUtils import set_attrib, run_hidden, clear_target
from SaveServer import load_config
from Parameters import load_parameters

# Carregar parâmetros do arquivo .ini
network_drive, server_drive, source, symbolic, junctions, label, folders_ignored = load_parameters()

# Variáveis definidas a partir do .ini
origem = source
destino_simbolico = symbolic
destino_juncoes = junctions
pastas_ignoradas = folders_ignored
labelX = label

def criar_juncoes(pastas):
    destino_simbolico.mkdir(parents=True, exist_ok=True)
    contador_sem_numero = 71
    padrao_numero = re.compile(r'^(\d{2})')

    for pasta in pastas:
        if pasta in pastas_ignoradas:
            continue

        caminho_origem = os.path.join(origem, pasta)
        if not os.path.isdir(caminho_origem):
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
    #print(f"Usuário logado: {usuario_logado}")

    # Carrega pastas salvas para o usuário
    usuario, selecionadas = load_config()

    if usuario != usuario_logado:
        print("⚠️ Nenhuma configuração encontrada para o usuário atual.")
        return

    if not selecionadas:
        print("⚠️ Nenhuma pasta selecionada para este usuário.")
        return

    #destino_simbolico = Path(r"X:\O")
    #destino_juncoes = Path(r"X:\\")
    clear_target(destino_simbolico, destino_juncoes)
    #print(f"Selecionadas: {selecionadas}")

    criar_juncoes(selecionadas)

    #save_config(usuario_logado, selecionadas)
    #openX()
    #print("✅ Junções aplicadas com sucesso e unidade X: aberta!")


if __name__ == "__main__":
    apply_junctions()
