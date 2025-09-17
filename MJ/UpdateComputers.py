import os
import re
import tempfile
from ftplib import FTP

# 🔽 Etapa 1: Configurações de FTP
ftp_host = "ftp.dicasapple.com"
ftp_user = "dicasa97"
ftp_pass = "CP1#F@b!@n0#"  # ⚠️ Substitua pela senha real
ftp_path = "/mjadvogados.net/wp/computers.txt"

# 🗂️ Caminho do arquivo temporário
temp_dir = tempfile.gettempdir()
arquivo_local = os.path.join(temp_dir, "computers_update.txt")

# 🖥️ Nome do computador atual
nome_computador = os.getenv("COMPUTERNAME") or os.uname().nodename

# 🛑 Nome a ser removido da lista
nome_a_remover = "Fabiano-GK3"

# 📥 Função para baixar o arquivo via FTP
def baixar_arquivo_ftp():
    print("🔽 Baixando arquivo do FTP...")
    with FTP(ftp_host) as ftp:
        ftp.login(user=ftp_user, passwd=ftp_pass)
        with open(arquivo_local, "wb") as f:
            ftp.retrbinary(f"RETR " + ftp_path, f.write)
    print("✅ Arquivo baixado com sucesso!")

# ✅ Chamada opcional: descomente para baixar do FTP
#baixar_arquivo_ftp()

try:
    # 🧠 Etapa 2: Ler e limpar o conteúdo
    with open(arquivo_local, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    # Remove linhas em branco e espaços extras
    linhas_limpas = [linha.strip() for linha in linhas if linha.strip()]

    # Remove qualquer linha que contenha "Fabiano-GK3"
    linhas_filtradas = [linha for linha in linhas_limpas if nome_a_remover not in linha]

    # Verifica se o computador atual já está na lista
    computador_ja_listado = any(nome_computador in linha for linha in linhas_filtradas)

    # Se não estiver, gera próximo MJ-xx com dois dígitos
    if not computador_ja_listado:
        codigos_mj = re.findall(r"MJ-(\d+)", "\n".join(linhas_filtradas))
        numeros_mj = sorted([int(n) for n in codigos_mj])
        proximo_mj = max(numeros_mj) + 1 if numeros_mj else 1
        novo_codigo_mj = f"MJ-{proximo_mj:02d}"  # ✅ Formato com dois dígitos
        nova_linha = f"{novo_codigo_mj}"
        linhas_filtradas.append(nova_linha)
        print(f"🆕 Computador adicionado: {nova_linha}")
    else:
        print(f"✅ Computador já está na lista: {nome_computador}")

    # 💾 Etapa 3: Salvar a atualização no arquivo temporário
    conteudo_atualizado = "\n".join(linhas_filtradas)
    with open(arquivo_local, "w", encoding="utf-8") as f:
        f.write(conteudo_atualizado)

    # 🔼 Etapa 4: Enviar o arquivo atualizado via FTP
    with FTP(ftp_host) as ftp:
        ftp.login(user=ftp_user, passwd=ftp_pass)
        with open(arquivo_local, "rb") as f:
            ftp.storbinary(f"STOR " + ftp_path, f)

    print("📤 Arquivo enviado com sucesso!")

finally:
    # 🧹 Etapa 5: Remove o arquivo temporário
    if os.path.exists(arquivo_local):
        pass
        #os.remove(arquivo_local)
