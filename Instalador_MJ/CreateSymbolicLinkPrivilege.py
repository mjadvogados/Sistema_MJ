import subprocess
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def grant_symlink_right():
    grupo = "Todos"  # ou "Everyone" se o sistema estiver em inglês
    comando = f'ntrights +r SeCreateSymbolicLinkPrivilege -u "{grupo}"'
    try:
        subprocess.run(comando, shell=True, check=True)
        print(f'Privilégio concedido ao grupo "{grupo}" com sucesso.')
    except subprocess.CalledProcessError as e:
        print("Erro ao executar o comando:", e)

if __name__ == "__main__":
    if not is_admin():
        print("Executando como administrador...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        grant_symlink_right()
