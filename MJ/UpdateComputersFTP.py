import os
import re
import tempfile
from ftplib import FTP

# 🔽 Etapa 1: Configurações de FTP
ftp_host = "ftp.dicasapple.com"
ftp_user = "dicasa97"
ftp_pass = "CP1#F@b!@n0#"  # ⚠️ Substitua pela senha real
ftp_path = "/mjadvogados.net/wp/computers.txt"

# 🗂️ Define o caminho do arquivo temporário
temp_dir = tempfile.gettempdir()
arquivo_local = os.path.join(temp_dir, "computers_update.txt")

try:
    # 🔽 Etapa 2: Baixar o arquivo via FTP
    #with FTP(ftp_host) as ftp:
        #ftp.login(user=ftp_user, passwd=ftp_pass)
        #with open(arquivo_local, "wb") as f:
            #ftp.retrbinary(f"RETR {ftp_path}", f.write)

    # 🧠 Etapa 3: Ler e analisar o conteúdo
    with open(arquivo_local, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()

    # 🔍 Busca por nomes no formato MJ-xx
    codigos_mj = re.findall(r"MJ-(\d{2})", conteudo)
    numeros_mj = sorted([int(n) for n in codigos_mj])

    if numeros_mj:
        ultimo_numero = numeros_mj[-1]
        novo_numero = ultimo_numero + 1
    else:
        novo_numero = 1

    novo_codigo = f"MJ-{novo_numero:02d}"
    conteudo_atualizado = conteudo + "\n" + novo_codigo

    # 💾 Etapa 4: Salvar a atualização no arquivo temporário
    with open(arquivo_local, "w", encoding="utf-8") as f:
        f.write(conteudo_atualizado)

    # 🔼 Etapa 5: Enviar o arquivo atualizado via FTP
    with FTP(ftp_host) as ftp:
        ftp.login(user=ftp_user, passwd=ftp_pass)
        with open(arquivo_local, "rb") as f:
            ftp.storbinary(f"STOR {ftp_path}", f)

    print(f"✅ Arquivo atualizado com sucesso! Novo código: {novo_codigo}")

finally:
    # 🧹 Etapa 6: Remove o arquivo temporário
    if os.path.exists(arquivo_local):
        #pass
        os.remove(arquivo_local)
