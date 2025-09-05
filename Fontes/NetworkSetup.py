# Login.py

import sys
from PyQt6.QtWidgets import QApplication
from AdminUtils import is_admin, relaunch_as_admin, activateadminaccount, hideaccountlogin
from FilesUtils import diskO
from SelectServer2 import SetServer
from LoginWindow import LoginWindow
from NetworkManager11 import start_main_window

def main():
    app = QApplication(sys.argv)

    # 2. Após login bem-sucedido, executa as verificações
    if not is_admin():
        relaunch_as_admin()



    # 1. Abre a janela de login primeiro
    login = LoginWindow()
    if not login.exec():
        print("Login cancelado. Encerrando o programa.")
        sys.exit(0)


    try:
        activateadminaccount()
        hideaccountlogin()
    except Exception:
        pass

    # 3. Verifica se a unidade O: está disponível
    if not diskO():
        select_server = SetServer()
        select_server.show()
        app.exec()

        if not diskO():
            print("Unidade O: ainda não disponível. Encerrando.")
            sys.exit(1)

    # 4. Abre a janela principal
    window = start_main_window()
    sys.exit(app.exec())

# 👇 ESSA LINHA É ESSENCIAL
if __name__ == "__main__":
    main()
