import requests
import re
from ftplib import FTP

# 🔽 Etapa 1: Baixar o arquivo via HTTP
http_url = "https://www.mjadvogados.net/computers.txt"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Cache-Control": "no-cache"
}


response = requests.get(http_url, headers=headers)
response.raise_for_status()
conteudo = response.text

# 🧠 Etapa 2: Atualizar o conteúdo com o próximo RG-xx
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
arquivo_local = "computers_update.txt"
with open(arquivo_local, "w", encoding="utf-8") as f:
    f.write(conteudo_atualizado)

# 🔼 Etapa 3: Enviar via FTP
ftp_host = "ftp.dicasapple.com"
ftp_user = "dicasa97"
ftp_pass = "CP1#F@b!@n0#"  # ⚠️ Substitua pela senha real
ftp_path = "/mjadvogados.net/wp/computers.txt"

with FTP(ftp_host) as ftp:
    ftp.login(user=ftp_user, passwd=ftp_pass)
    with open(arquivo_local, "rb") as f:
        ftp.storbinary(f"STOR {ftp_path}", f)

print(f"✅ Arquivo atualizado com sucesso! Novo código: {novo_codigo}")
