import winreg
import subprocess
import time

def ocultar_arquivos_ocultos():
    try:
        # Caminho da chave
        chave = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
        
        # Abrir a chave com permissão de escrita
        registro = winreg.OpenKey(winreg.HKEY_CURRENT_USER, chave, 0, winreg.KEY_SET_VALUE)
        
        # Definir valor 2 para ocultar arquivos ocultos
        winreg.SetValueEx(registro, "Hidden", 0, winreg.REG_DWORD, 2)
        winreg.CloseKey(registro)
        
        print("✔ Arquivos ocultos não serão mais exibidos no Explorer.")
    except Exception as e:
        print(f"❌ Erro ao modificar o registro: {e}")

def reiniciar_explorer():
    try:
        print("⏳ Reiniciando o Windows Explorer...")
        # Finaliza o processo explorer.exe
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)  # Aguarda 2 segundos
        # Reinicia o explorer.exe
        subprocess.run(["start", "explorer"], shell=True)
        print("✅ Windows Explorer reiniciado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao reiniciar o Explorer: {e}")

# Executa as funções
ocultar_arquivos_ocultos()
reiniciar_explorer()
