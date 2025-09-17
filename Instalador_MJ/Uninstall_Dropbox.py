import subprocess
import winreg
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox


def get_dropbox_uninstall_cmd():
    """
    Busca no Registro o comando de desinstalação do Dropbox.
    Retorna o comando formatado para execução silenciosa, ou None se não encontrado.
    """
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for root in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
        for path in registry_paths:
            try:
                with winreg.OpenKey(root, path) as key:
                    for i in range(0, winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                if "Dropbox" in display_name:
                                    uninstall_cmd, _ = winreg.QueryValueEx(subkey, "UninstallString")
                                    return uninstall_cmd
                        except FileNotFoundError:
                            continue
                        except Exception:
                            continue
            except Exception:
                continue
    return None


def uninstall_dropbox_silently(uninstall_cmd):
    """
    Executa a desinstalação em modo silencioso sem abrir terminal.
    """
    try:
        if "msiexec" in uninstall_cmd.lower():
            args = uninstall_cmd + " /quiet /norestart"
        else:
            args = f'"{uninstall_cmd}" /S'

        subprocess.run(args, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except Exception:
        return False


def show_message(title, message, icon):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(icon)
    msg.exec()


def main():
    app = QApplication(sys.argv)

    cmd = get_dropbox_uninstall_cmd()
    if not cmd:
        show_message("Dropbox", "Dropbox não encontrado no sistema.", QMessageBox.Icon.Warning)
        sys.exit()

    success = uninstall_dropbox_silently(cmd)
    if success:
        show_message("Dropbox", "Dropbox foi desinstalado com sucesso.", QMessageBox.Icon.Information)
    else:
        show_message("Dropbox", "Erro ao tentar desinstalar o Dropbox.", QMessageBox.Icon.Critical)

    sys.exit()


if __name__ == "__main__":
    main()
