import sys
import os
import ctypes
import subprocess
import shutil
import time
import win32gui, win32con
import winreg
from pathlib import Path
import win32com.client



def set_attrib(path, ocultar=True):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    FILE_ATTRIBUTE_SYSTEM = 0x04
    attrs = FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM if ocultar else 0
    ctypes.windll.kernel32.SetFileAttributesW(str(path), attrs)


def run_hidden(cmd):
    subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)


def check_folder(folder):
    folder.mkdir(parents=True, exist_ok=True)

def checkX():
    return os.path.isdir("X:\\")

def check_disk(letra_unidade):
    caminho = f"{letra_unidade.upper()}:\\"
    return os.path.isdir(letra_unidade)

def clear_target(simbolico, juncoes):
    set_attrib(simbolico, ocultar=False)

    if simbolico.exists():
        for item in simbolico.glob("*"):
            run_hidden(f'rmdir /S /Q "{item}"')
        shutil.rmtree(simbolico, ignore_errors=True)
    simbolico.mkdir(parents=True, exist_ok=True)

    if juncoes.exists():
        for item in juncoes.glob("*"):
            run_hidden(f'rmdir /S /Q "{item}"')

def openX(janela):
    try:
        import win32gui
        import win32con

        janela_encontrada = []

        def enum_callback(hwnd, _):
            titulo = win32gui.GetWindowText(hwnd)
            classe = win32gui.GetClassName(hwnd)
            if "Servidor (X:)" in titulo and "CabinetWClass" in classe:
                janela_encontrada.append(hwnd)

        win32gui.EnumWindows(enum_callback, None)

        for hwnd in janela_encontrada:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

        # Espera a janela fechar antes de abrir novamente
        import time
        time.sleep(1)

        run_hidden('explorer "X:\\"')

    except Exception:
        run_hidden('explorer "X:\\"')

    janela.selecionar_pastas()


def diskO():
    caminho = r"O:\\"  # Dupla barra para escapar corretamente
    return os.path.isdir(caminho)

def drive_label(drive_letter, label):
    shell = win32com.client.Dispatch("Shell.Application")
    shell.NameSpace(drive_letter).Self.Name = label

def hide_drive(letter):
    """
    Oculta uma unidade de disco no Windows modificando a chave de registro NoDrives.

    Parâmetro:
    - letter: Letra da unidade a ser ocultada (ex: 'O')
    """
    letter = letter.upper()
    posicao = ord(letter) - ord('A')
    bitmask = 1 << posicao  # Cria máscara binária para a letra

    chave_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"

    try:
        chave = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            chave_path,
            0,
            winreg.KEY_READ | winreg.KEY_SET_VALUE
        )
    except FileNotFoundError:
        chave = winreg.CreateKey(
            winreg.HKEY_LOCAL_MACHINE,
            chave_path
        )
        valor_atual = 0
    else:
        try:
            valor_atual, _ = winreg.QueryValueEx(chave, "NoDrives")
        except FileNotFoundError:
            valor_atual = 0

    novo_valor = valor_atual | bitmask

    try:
        winreg.SetValueEx(chave, "NoDrives", 0, winreg.REG_DWORD, novo_valor)
    except PermissionError:
        print("❌ Permissão negada ao tentar modificar NoDrives. Execute como administrador.")
    finally:
        winreg.CloseKey(chave)

