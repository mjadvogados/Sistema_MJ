import os
import winreg
import shutil
import psutil
import time

# Função para remover entradas do registro de inicialização
def remove_dropbox_registry_startup():
    try:
        # Remover Dropbox da chave de inicialização do usuário (HKCU)
        reg_path_user = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path_user, 0, winreg.KEY_SET_VALUE) as reg_key:
            try:
                # Tentar remover a entrada "Dropbox"
                winreg.DeleteValue(reg_key, "Dropbox")
                print("Entrada 'Dropbox' removida da inicialização (HKCU).")
            except FileNotFoundError:
                print("Entrada 'Dropbox' não encontrada no registro (HKCU).")
            
            try:
                # Tentar remover a entrada "DropboxStart"
                winreg.DeleteValue(reg_key, "DropboxStart")
                print("Entrada 'DropboxStart' removida da inicialização (HKCU).")
            except FileNotFoundError:
                print("Entrada 'DropboxStart' não encontrada no registro (HKCU).")

        # Remover Dropbox da chave de inicialização para todos os usuários (HKLM)
        reg_path_machine = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path_machine, 0, winreg.KEY_SET_VALUE) as reg_key:
            try:
                # Tentar remover a entrada "Dropbox"
                winreg.DeleteValue(reg_key, "Dropbox")
                print("Entrada 'Dropbox' removida da inicialização (HKLM).")
            except FileNotFoundError:
                print("Entrada 'Dropbox' não encontrada no registro (HKLM).")
            
            try:
                # Tentar remover a entrada "DropboxStart"
                winreg.DeleteValue(reg_key, "DropboxStart")
                print("Entrada 'DropboxStart' removida da inicialização (HKLM).")
            except FileNotFoundError:
                print("Entrada 'DropboxStart' não encontrada no registro (HKLM).")
    
    except PermissionError:
        print("Erro de permissão: Execute o script como Administrador para remover entradas do registro.")
    except Exception as e:
        print(f"Erro ao remover entradas do registro: {e}")

# Função para remover Dropbox da pasta de inicialização
def remove_dropbox_startup_shortcut():
    startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    dropbox_shortcut = os.path.join(startup_folder, "Dropbox.lnk")
    
    if os.path.exists(dropbox_shortcut):
        try:
            os.remove(dropbox_shortcut)
            print("Atalho do Dropbox removido da inicialização (pasta de Startup).")
        except Exception as e:
            print(f"Erro ao remover atalho de inicialização do Dropbox: {e}")
    else:
        print("Atalho de inicialização do Dropbox não encontrado na pasta Startup.")

# Função principal
def main():
    remove_dropbox_registry_startup()  # Remover entradas no registro de inicialização
    remove_dropbox_startup_shortcut()  # Remover atalho na pasta de inicialização
    
    print("O Dropbox foi removido da inicialização automática.")

if __name__ == "__main__":
    main()
