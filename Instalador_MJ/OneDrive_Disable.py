import sys
import subprocess
import winreg
import ctypes
from PyQt6.QtWidgets import QApplication, QMessageBox


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def kill_onedrive():
    subprocess.call(["taskkill", "/f", "/im", "OneDrive.exe"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def remove_onedrive_from_startup():
    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
            try:
                winreg.DeleteValue(key, "OneDrive")
                return "Entrada de inicialização removida com sucesso."
            except FileNotFoundError:
                return "OneDrive não estava na inicialização automática."
    except Exception as e:
        return f"Erro ao remover da inicialização: {e}"


def hide_onedrive_from_explorer():
    try:
        # Remove o ícone da navegação lateral (apenas visual, não impede execução)
        nav_key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel"
        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, nav_key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "{018D5C66-4533-4307-9B53-224DE2ED1FE6}", 0, winreg.REG_DWORD, 1)

        # Tenta remover da barra lateral (Explorer NameSpace) — visual apenas
        explorer_keys = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{018D5C66-4533-4307-9B53-224DE2ED1FE6}",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{018D5C66-4533-4307-9B53-224DE2ED1FE6}"
        ]
        for key_path in explorer_keys:
            try:
                winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            except FileNotFoundError:
                continue

        return "Ícone do OneDrive removido da barra lateral do Explorer."
    except PermissionError:
        return "Permissão negada ao alterar o registro. Execute como administrador."


def allow_manual_onedrive_execution():
    try:
        key_path = r"SOFTWARE\Policies\Microsoft\Windows\OneDrive"
        with winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, "DisableFileSync", 0, winreg.REG_DWORD, 0)
        return "OneDrive pode ser executado manualmente pelo usuário."
    except PermissionError:
        return "Erro ao permitir execução manual do OneDrive. Execute como administrador."


def main():
    app = QApplication(sys.argv)

    if not is_admin():
        QMessageBox.critical(None, "Erro", "Este script precisa ser executado como administrador.")
        sys.exit(1)

    kill_onedrive()

    result1 = remove_onedrive_from_startup()
    result2 = hide_onedrive_from_explorer()
    result3 = allow_manual_onedrive_execution()

    summary = "\n".join([result1, result2, result3, "Reinicie o computador para aplicar as alterações."])
    QMessageBox.information(None, "OneDrive Desativado", summary)

    sys.exit(0)


if __name__ == "__main__":
    main()
