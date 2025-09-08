import py7zr
import os

def descompactar_arquivo_7z(caminho_arquivo, destino, senha=None):
    if not os.path.exists(destino):
        os.makedirs(destino)

    try:
        with py7zr.SevenZipFile(caminho_arquivo, mode='r', password=senha) as arquivo:
            arquivo.extractall(path=destino)
        print(f"✅ Arquivo '{caminho_arquivo}' descompactado em '{destino}'")
    except py7zr.exceptions.PasswordRequired:
        print(f"❌ O arquivo '{caminho_arquivo}' requer uma senha e nenhuma foi fornecida.")
    except py7zr.exceptions.InvalidPassword:
        print(f"❌ Senha incorreta para o arquivo '{caminho_arquivo}'.")
    except Exception as e:
        print(f"⚠️ Erro ao descompactar '{caminho_arquivo}': {e}")

# 🔍 Exemplo de uso
caminho_arquivo_7z = 'exemplo_com_ou_sem_senha.7z'
pasta_destino = 'saida_descompactada'
senha_opcional = 'minha_senha'  # ou None se não tiver senha

descompactar_arquivo_7z(caminho_arquivo_7z, pasta_destino, senha=senha_opcional)
