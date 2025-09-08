import os
import sys
import re
import ast
import configparser
from pathlib import Path
from FilesUtils import set_attrib, run_hidden, clear_target
from SaveServer import load_config
from Parameters import load_parameters
# Caminho para os arquivos de configuração
CONFIG_DIR = r"C:\ProgramData\NetworkManager"
CONFIG_PROGRAM = os.path.join(CONFIG_DIR, "ConfigProgram.ini")
CONFIG_FOLDERS = os.path.join(CONFIG_DIR, "ConfigFolders.ini")


def ler_configuracoes():
    # Lê parâmetros do arquivo ConfigProgram.ini
    config_program = configparser.ConfigParser()
    config_program.read(CONFIG_PROGRAM, encoding="latin-1")

    params = config_program["Parameters"]
    network_drive = params.get("network_drive")
    server_drive = params.get("server_drive")
    source = Path(params.get("source")).resolve()
    symbolic = Path(params.get("symbolic")).resolve()
    junctions = Path(params.get("junctions")).resolve()
    label = params.get("label")
    folders_ignored_str = params.get("folders_ignored", "{}")

    network_drive, server_drive, source, symbolic, junctions, label, folders_ignored = load_parameters()
    # Usar ast.literal_eval para segurança
    folders_ignored = ast.literal_eval(folders_ignored_str)

    user_name,  selected_folders = load_config()
    return {
        "network_drive": network_drive,
        "server_drive": server_drive,
        "source": source,
        "symbolic": symbolic,
        "junctions": junctions,
        "label": label,
        "folders_ignored": folders_ignored,
        "user_name": user_name,
        "selected_folders": selected_folders
    }


def criar_juncoes(source, symbolic, junctions, selected_folders, folders_ignored):
    print("📁 Iniciando criação de junções...")
    symbolic.mkdir(parents=True, exist_ok=True)

    contador_sem_numero = 71
    padrao_numero = re.compile(r'^(\d{2})')

    for pasta in selected_folders:
        if pasta in folders_ignored:
            #print(f"⏭️  Ignorando pasta: {pasta}")
            continue

        caminho_origem = source / pasta
        if not caminho_origem.exists():
            print(f"⚠️  Pasta não encontrada: {caminho_origem}")
            continue

        match = padrao_numero.match(pasta)
        if match:
            nome_link = match.group(1)
        else:
            if contador_sem_numero > 89:
                print("❌ Número máximo de pastas sem numeração excedido. Operação cancelada.")
                return
            nome_link = f"{contador_sem_numero:02d}"
            contador_sem_numero += 1

        link = symbolic / nome_link
        juncao = junctions / pasta

        #print(f"🔗 Criando link simbólico: {link} -> {caminho_origem}")
        run_hidden(f'mklink /D "{link}" "{caminho_origem}"')

        #print(f"🔗 Criando junção: {juncao} -> {link}")
        run_hidden(f'mklink /J "{juncao}" "{link}"')

    set_attrib(symbolic)
    print("✅ Junções criadas com sucesso!")


def main():
    print("🔍 Lendo arquivos de configuração...")
    config = ler_configuracoes()

    usuario_logado = os.getlogin().strip()
    usuario_configurado = config["user_name"].strip()

    if usuario_logado.lower() != usuario_configurado.lower():
        print(f"🚫 Usuário atual: '{usuario_logado}' não corresponde ao usuário permitido no .ini: '{usuario_configurado}'.")
        print("🔒 Operação cancelada por segurança.")
        return

    print(f"👤 Usuário autenticado: {usuario_logado}")
    print(f"📁 Pastas selecionadas para junção: {config['selected_folders']}")
    print(f"🚫 Pastas ignoradas: {config['folders_ignored']}")

    # Limpa links existentes
    print("🧹 Limpando links e junções anteriores...")
    clear_target(config["symbolic"], config["junctions"])

    # Aplica as novas junções
    criar_juncoes(
        config["source"],
        config["symbolic"],
        config["junctions"],
        config["selected_folders"],
        config["folders_ignored"]
    )


if __name__ == "__main__":
    main()
