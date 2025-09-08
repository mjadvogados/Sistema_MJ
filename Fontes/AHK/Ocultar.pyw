import winreg
import subprocess
import os
from datetime import datetime

def ocultar_arquivos_ocultos():
    try:
        chave = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
        registro = winreg.OpenKey(winreg.HKEY_CURRENT_USER, chave, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(registro, "Hidden", 0, winreg.REG_DWORD, 2)
        winreg.CloseKey(registro)
        return "✔ Arquivos ocultos desativados com sucesso."
    except Exception as e:
        return f"❌ Erro ao modificar o registro: {e}"

def reiniciar_explorer():
    try:
        subprocess.run(
            ["taskkill", "/f", "/im", "explorer.exe"],
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ["explorer.exe"],
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return "✅ Windows Explorer reiniciado."
    except Exception as e:
        return f"❌ Erro ao reiniciar o Explorer: {e}"

def gravar_log(mensagem):
    try:
        pasta_log = r"C:\Winddows\Logs"
        os.makedirs(pasta_log, exist_ok=True)
        caminho_log = os.path.join(pasta_log, "ocultar_arquivos.log")
        with open(caminho_log, "a", encoding="utf-8") as log:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log.write(f"[{timestamp}] {mensagem}\n")
    except:
        pass

# Executa tudo
msg1 = ocultar_arquivos_ocultos()
msg2 = reiniciar_explorer()
gravar_log(msg1)
gravar_log(msg2)
