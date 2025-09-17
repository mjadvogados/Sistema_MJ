import sys
import os
import subprocess
import winreg
import ctypes
from PyQt6.QtWidgets import QApplication, QMessageBox


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def restore_onedrive_registry():
    try:
        key_path = r"SOFTWARE\Policies\Microsoft\Windows\OneDrive"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, "DisableFileSync", 0, winreg.REG_DWORD, 0)
        return "OneDrive reativado no registro com sucesso."
    except FileNotFoundError:
        return "Chave de política do OneDrive não existia. Nenhuma alteração feita."
    except PermissionError:
        return "Erro ao reativar o OneDrive. Execute como administrador."


def restore_explorer_icon():
    try:
        name_space_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace"
        with winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE,
                                os.path.join(name_space_path, r"{018D5C66-4533-4307-9B53-224DE2ED1FE6}"),
                                0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, None, 0, winreg.REG_SZ, "OneDrive")

        # Remove ocultamento da navegação lateral
        nav_key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, nav_key_path, 0, winreg.KEY_ALL_ACCESS) as key:
                winreg.DeleteValue(key, "{018D5C66-4533-4307-9B53-224DE2ED1FE6}")
        except FileNotFoundError:
            pass  # Valor não existe, tudo bem

        return "Ícone do OneDrive restaurado no Explorer."
    except Exception as e:
        return f"Erro ao restaurar ícone no Explorer: {e}"


def restore_onedrive_startup():
    try:
        # Caminho do executável do OneDrive
        onedrive_path = os.path.expandvars(r"%LocalAppData%\Microsoft\OneDrive\OneDrive.exe")
        if not os.path.exists(onedrive_path):
            return "OneDrive não está instalado neste usuário."

        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, "OneDrive", 0, winreg.REG_SZ, f"\"{onedrive_path}\" /background")

        return "OneDrive restaurado na inicialização automática."
    except Exception as e:
        return f"Erro ao restaurar inicialização do OneDrive: {e}"


def main():
    app = QApplication(sys.argv)

    if not is_admin():
        QMessageBox.critical(None, "Erro", "Este script precisa ser executado como administrador.")
        sys.exit(1)

    result1 = restore_onedrive_registry()
    result2 = restore_explorer_icon()
    result3 = restore_onedrive_startup()

    summary = "\n".join([result1, result2, result3, "Reinicie o computador para concluir a restauração."])
    QMessageBox.information(None, "OneDrive Restaurado", summary)

    sys.exit(0)


if __name__ == "__main__":
    main()
