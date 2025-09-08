import os
import subprocess
import time

# Constante para ocultar janelas de subprocessos no Windows
CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW

def unidade_disponivel(unidade):
    return os.path.exists(unidade)

def executar_autorun():
    autorun_path = r"C:\Windows\MJ\Autorun.exe"
    subprocess.Popen([autorun_path], shell=True, creationflags=CREATE_NO_WINDOW)

def abrir_explorer(unidade):
    subprocess.Popen(["explorer", unidade], shell=True, creationflags=CREATE_NO_WINDOW)

def main():
    unidade_o = "O:\\"
    unidade_x = "X:\\"

    if not (unidade_disponivel(unidade_o) and unidade_disponivel(unidade_x)):
        executar_autorun()
        time.sleep(12)  # Espera inicial para o autorun.exe finalizar

    # Verifica novamente as unidades até um limite de tentativas
    for _ in range(15):  # Total de até 30 segundos (15 x 2s)
        if unidade_disponivel(unidade_o) and unidade_disponivel(unidade_x):
            abrir_explorer(unidade_x)
            return
        time.sleep(3)

if __name__ == "__main__":
    main()
