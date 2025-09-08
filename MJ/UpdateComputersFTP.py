import sys
import os
import re
from ftplib import FTP

# 🔽 Etapa 1: Baixar o arquivo via FTP
ftp_host = "ftp.dicasapple.com"
ftp_user = "dicasa97"
ftp_pass = "CP1#F@b!@n0#"  # ⚠️ Substitua pela senha real
ftp_path = "/mjadvogados.net/wp/computers.txt"
arquivo_local = "computers_update.txt"

with FTP(ftp_host) as ftp:
    ftp.login(user=ftp_user, passwd=ftp_pass)
    with open(arquivo_local, "wb") as f:
        ftp.retrbinary(f"RETR {ftp_path}", f.write)


# 🧠 Etapa 2: Atualizar o conteúdo com o próximo RG-xx
with open(arquivo_local, "r", encoding="utf-8") as f:
    conteudo = f.read()

codigos = re.findall(r"RG-(\d+)", conteudo)
numeros = [int(n) for n in codigos]
proximo_numero = max(numeros) + 1 if numeros else 1
novo_codigo = f"RG-{proximo_numero}"

# Evita duplicação
if novo_codigo not in conteudo:
    conteudo_atualizado = conteudo.strip() + "\n" + novo_codigo
else:
    conteudo_atualizado = conteudo

# Salva localmente
with open(arquivo_local, "w", encoding="utf-8") as f:
    f.write(conteudo_atualizado)

# 🔼 Etapa 3: Enviar via FTP
with FTP(ftp_host) as ftp:
    ftp.login(user=ftp_user, passwd=ftp_pass)
    with open(arquivo_local, "rb") as f:
        ftp.storbinary(f"STOR {ftp_path}", f)

print(f"✅ Arquivo atualizado com sucesso! Novo código: {novo_codigo}")
os.remove(arquivo_local)