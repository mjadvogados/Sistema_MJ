import subprocess

def change_label(letra_unidade: str, rotulo_novo: str):
    letra = letra_unidade.replace(":", "").upper()
    
    # Monta o comando PowerShell como string
    comando_powershell = f'label {letra}: "{rotulo_novo}"'
    
    # Executa o comando PowerShell de forma oculta e sem saída
    subprocess.run(
        ["powershell", "-WindowStyle", "Hidden", "-Command", comando_powershell],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
