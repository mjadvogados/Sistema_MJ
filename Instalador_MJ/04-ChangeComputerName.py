import subprocess

def renomear_computador_windows(novo_nome):
    # Comando PowerShell para renomear o computador
    comando_powershell = [
        "powershell",
        "-Command",
        f'Rename-Computer -NewName "{novo_nome}" -Force'
    ]

    # Executa o comando sem abrir janela
    try:
        subprocess.run(
            comando_powershell,
            shell=False,
            creationflags=subprocess.CREATE_NO_WINDOW,
            check=True
        )
    except subprocess.CalledProcessError:
        pass  # Silenciosamente ignora falhas

# Exemplo de uso (pode ser chamado de outro módulo):
renomear_computador_windows("FABIANO-PC")
