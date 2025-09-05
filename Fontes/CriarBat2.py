import os
import subprocess

def create_bat(server):
    # Garante que a pasta C:\MJ-Network exista
    pasta_destino = r"C:\MJ-Network"
    os.makedirs(pasta_destino, exist_ok=True)

    # Caminho completo do arquivo
    caminho_arquivo = os.path.join(pasta_destino, "MJ.bat")

    # Conteúdo do arquivo BAT
    conteudo = f"""@echo off
chcp 1252
net use * /delete /yes > nul
net use O: {server} /user:administrador mj2145mj /persistent:yes
exit /b %errorlevel%
"""

    # Escreve o conteúdo no arquivo
    with open(caminho_arquivo, "w") as arquivo:
        arquivo.write(conteudo)

    print(f"Arquivo MJ.bat criado em: {caminho_arquivo}")
    return caminho_arquivo

def executar_bat(caminho_bat):
    try:
        resultado = subprocess.run(
            [caminho_bat],
            shell=True,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # <- evita abrir janela de terminal
        )

        if resultado.returncode == 0:
            print("Execução bem-sucedida!")
            return True
        else:
            print(f"Falha na execução. Código de saída: {resultado.returncode}")
            print("Erros:", resultado.stderr.strip())
            return False

    except Exception as e:
        print(f"Erro ao executar o .bat: {e}")
        return False

# Exemplo de uso
servidor_input = r"\\servidor-rg\o$"
caminho_bat = create_bat(servidor_input)
sucesso = executar_bat(caminho_bat)
