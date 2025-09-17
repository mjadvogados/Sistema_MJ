import os
import psutil
import shutil
import winreg
import time

# Função para parar o serviço do Dropbox e todos os processos relacionados
def stop_dropbox_service():
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if 'Dropbox' in proc.info['name']:
            print(f"Parando processo: {proc.info['name']} (PID: {proc.info['pid']})")
            proc.terminate()
            proc.wait()  # Aguarda o término do processo
            time.sleep(1)  # Atraso para garantir que o processo foi encerrado

# Função para tentar remover o arquivo bloqueado (usando os módulos os e psutil)
def remove_file_if_locked(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)  # Tenta excluir o arquivo
            print(f"Arquivo {file_path} removido com sucesso.")
    except PermissionError:
        print(f"Erro ao remover {file_path}: Arquivo em uso. Tentando liberar o bloqueio.")
        # Tenta forçar a liberação do arquivo
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            for file in proc.open_files():
                if file.path == file_path:
                    print(f"Arquivo {file_path} está em uso por {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()  # Tenta encerrar o processo que está usando o arquivo
                    proc.wait()  # Espera o processo terminar
                    time.sleep(1)
                    try:
                        os.remove(file_path)  # Tenta remover novamente
                        print(f"Arquivo {file_path} removido com sucesso após liberar o bloqueio.")
                    except Exception as e:
                        print(f"Falha ao remover {file_path} após liberar o bloqueio: {e}")

# Função para remover as pastas do Dropbox
def remove_dropbox_folders():
    dropbox_paths = [
        r"C:\Program Files (x86)\Dropbox",
        r"C:\Users\{user}\AppData\Roaming\Dropbox",
        r"C:\Users\{user}\AppData\Local\Dropbox",
        r"C:\Users\{user}\Dropbox"
    ]
    user_profile = os.environ.get("USERPROFILE", "C:\\Users\\Default")  # Pega o perfil do usuário atual
    
    for path in dropbox_paths:
        path = path.format(user=user_profile.split("\\")[-1])  # Substitui o {user} pelo nome do usuário atual
        if os.path.exists(path):
            try:
                print(f"Removendo pasta: {path}")
                shutil.rmtree(path)
            except Exception as e:
                print(f"Erro ao remover {path}: {e}")
                # Se houver erro, tenta remover arquivos específicos que possam estar em uso
                if 'DropboxExt64.79.0.dll' in str(e):
                    remove_file_if_locked(os.path.join(path, 'DropboxExt64.79.0.dll'))

# Função para remover entradas do registro
def remove_dropbox_registry():
    try:
        # HKEY_CURRENT_USER (HKCU)
        reg_path_user = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Dropbox"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path_user, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.DeleteKey(reg_key, "")
        print("Entrada do registro (HKCU) removida.")
        
        # HKEY_LOCAL_MACHINE (HKLM)
        reg_path_machine = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Dropbox"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path_machine, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.DeleteKey(reg_key, "")
        print("Entrada do registro (HKLM) removida.")
        
    except FileNotFoundError:
        print("Entradas do registro do Dropbox não encontradas.")
    except PermissionError:
        print("Erro: Permissão negada ao tentar acessar o registro. Execute como administrador.")
    except Exception as e:
        print(f"Erro ao remover entradas do registro: {e}")

# Função principal que executa a remoção completa
def main():
    stop_dropbox_service()  # Parar o serviço do Dropbox
    remove_dropbox_folders()  # Remover pastas do Dropbox
    remove_dropbox_registry()  # Remover entradas do registro
    
    print("Remoção do Dropbox concluída.")

if __name__ == "__main__":
    main()
