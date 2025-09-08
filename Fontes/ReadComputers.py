import requests
import re

url = "https://www.mjadvogados.net/computers.txt"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Cache-Control": "no-cache"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    conteudo = response.text

    # Normaliza o conteúdo para evitar espaços extras
    linhas = [linha.strip() for linha in conteudo.splitlines() if linha.strip()]
    
    # Captura todos os códigos RG-xx corretamente
    codigos = re.findall(r"RG-\d+", "\n".join(linhas))

    if codigos:
        # Extrai os números e encontra o maior
        numeros = [int(codigo.split("-")[1]) for codigo in codigos]
        maior_numero = max(numeros)
        novo_codigo = f"RG-{maior_numero + 1}"

        # Verifica se o novo código já existe (por segurança)
        if novo_codigo in codigos:
            print(f"O código '{novo_codigo}' já existe na lista. Nenhuma alteração feita.")
        else:
            novo_conteudo = conteudo.strip() + "\n" + novo_codigo
            with open("computers_update.txt", "w", encoding="utf-8") as f:
                f.write(novo_conteudo)
            print(f"Novo código '{novo_codigo}' adicionado e salvo em 'computers_update.txt'.")
    else:
        print("Nenhum código no formato 'RG-xx' encontrado.")

except requests.exceptions.RequestException as e:
    print(f"Erro ao acessar o arquivo: {e}")
