import sys
import os
import ctypes
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QFrame, QStatusBar
)
from PyQt6.QtCore import Qt, QCoreApplication

#from MapNetwork import map_drive
from SaveServer import save_server
from CreateBat import create_bat
from FilesUtils import run_hidden
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def relaunch_as_admin():
    script = sys.executable
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 1)


class SetServer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MJ Advogados - Seleção de Servidor")
        self.setFixedSize(500, 400)

        # ❌ Removido WA_TranslucentBackground para fundo sólido
        # ❌ Mantido FramelessWindowHint para barra de título personalizada
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # ✅ Fundo laranja sólido com bordas arredondadas
        self.setStyleSheet("""
            QMainWindow {
                background-color: orange;
                border: 3px solid red;
                border-radius: 15px;
            }
        """)

        self.center_window()

        # Frame principal
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 500, 400)

        # Barra de título personalizada
        self.title_label = QLabel("MJ Advogados - Seleção de Servidor", self.frame)
        self.title_label.setGeometry(0, 0, 500, 40)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            background-color: darkred;
            color: white;
            font-weight: bold;
            font-size: 14pt;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
        """)

        # Label "Selecionar servidor"
        self.server_label = QLabel("Selecionar servidor", self.frame)
        self.server_label.setGeometry(30, 70, 200, 30)
        self.server_label.setStyleSheet("color: black; font-size: 13pt;")

        # ComboBox
        self.combo = QComboBox(self.frame)
        self.combo.setGeometry(30, 100, 200, 30)
        self.combo.addItems([
            "Pelotas", "Pelotas (backup)", "Rio Grande", "Rio Grande (backup)",
            "Santa Vitória", "Santa Vitória (backup)"
        ])
        self.combo.setAccessibleName("Seleção de servidor")
        self.combo.setToolTip("Escolha o servidor desejado para conexão")
        self.combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                font-size: 13pt;
                padding: 2px;
                border: 1px solid gray;
                border-radius: 5px;
            }
        """)

        # ✅ Botões com bordas arredondadas e efeito 3D
        self.apply_button = QPushButton("&Aplicar", self.frame)
        self.close_button = QPushButton("&Fechar", self.frame)

        button_style = """
            QPushButton {
                background-color: navy;
                color: white;
                font-weight: bold;
                font-size: 12pt;
                border-radius: 10px;
                border: 2px outset lightgray;
                padding: 5px;
            }
            QPushButton:pressed {
                border: 2px inset lightgray;
                background-color: #000080;
            }
        """
        self.apply_button.setStyleSheet(button_style)
        self.close_button.setStyleSheet(button_style)

        # Posicionamento dos botões
        button_width = 100
        button_height = 40
        spacing = 20
        total_width = button_width * 2 + spacing
        x_start = (500 - total_width) // 2
        y_pos = 280

        self.apply_button.setGeometry(x_start, y_pos, button_width, button_height)
        self.close_button.setGeometry(x_start + button_width + spacing, y_pos, button_width, button_height)

        self.close_button.clicked.connect(self.close)
        self.apply_button.clicked.connect(self.aplicar_servidor)

        # Barra de status real do QMainWindow
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("""
            background-color: yellow;
            color: black;
            font-weight: bold;
            font-size: 12pt;
        """)
        self.status_bar.showMessage("© 2025 - Fabiano Fonseca")

    def aplicar_servidor(self):
        servidor = self.combo.currentText().lower()
        if servidor == "pelotas":
            caminho = r"\\servidor-pel\o$"
        elif servidor == "pelotas (backup)":
            caminho = r"\\pelotas-01\o$"
        elif servidor == "santa vitória":
            caminho = r"\\servidor-svp\o$"
        elif servidor == "rio grande":
            caminho = r"\\servidor\o$"
        elif servidor == "rio grande (backup)":
            caminho = r"\\rg-05\o$"
        else:
            caminho = ""
            return

        #map_drive(caminho, "O")
        save_server(caminho)
        create_bat(caminho)
        run_hidden(r"C:\MJ-Network\MJ.bat")
        if os.path.exists("O:"):
            print("Unidade de rede Ok")
        else:
            print("Erro ao acessar a unidade de rede")
            return

    def center_window(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)


if __name__ == "__main__":
    if not is_admin():
        relaunch_as_admin()
        sys.exit()

    app = QApplication(sys.argv)
    window = SetServer()
    window.show()
    sys.exit(app.exec())
