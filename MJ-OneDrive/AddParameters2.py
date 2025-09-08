import sys
import configparser
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFrame, QStatusBar
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

INI_PATH = r"C:\ProgramData\NetworkManager\OneDriveConfig.ini"

class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(600, 460)
        self.setStyleSheet("""
            QWidget {
                background-color: orange;
                border: 4px solid lightcoral;
                border-radius: 15px;
            }
        """)
        self.center_window()
        self.setWindowTitle("MJ Advogados - Cadastro de Parâmetros - OneDrive Online")

        self.init_ui()
        self.load_config()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def init_ui(self):
        # Barra de título personalizada
        self.title_bar = QLabel("MJ Advogados - Cadastro de Parâmetros - OneDrive Online", self)
        self.title_bar.setGeometry(0, 0, self.width(), 40)
        self.title_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_bar.setStyleSheet("""
            QLabel {
                background-color: darkred;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }
        """)

        # Frame principal
        self.frame = QFrame(self)
        self.frame.setGeometry(10, 50, 580, 350)

        font_label = QFont()
        font_label.setBold(True)

        # Campos
        self.fields = {}
        labels = {
            "origem": "Origem",
            "destino_simbolico": "Destino Simbólico",
            "destino_juncoes": "Destino Junções",
            "label": "Label",
            "caminhovhdx": "Caminho VHDX",
            "icone": "Ícone"
        }

        y = 10
        for key, text in labels.items():
            lbl = QLabel(text, self.frame)
            lbl.setFont(font_label)
            lbl.setStyleSheet("color: black;")
            lbl.setGeometry(20, y, 200, 20)

            field = QLineEdit(self.frame)
            field.setGeometry(20, y + 25, 540, 30)
            field.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    color: black;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)
            field.setAccessibleName(text)
            self.fields[key] = field
            y += 70

        # Botões
        self.btn_save = QPushButton("Salvar", self)
        self.btn_close = QPushButton("Fechar", self)

        for btn in [self.btn_save, self.btn_close]:
            btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: navy;
                    color: white;
                    border-radius: 10px;
                    padding: 8px 16px;
                    border: 2px solid #000;
                }
                QPushButton:hover {
                    background-color: #000080;
                }
            """)

        self.btn_save.setGeometry(180, 410, 100, 30)
        self.btn_close.setGeometry(320, 410, 100, 30)

        self.btn_save.clicked.connect(self.save_config)
        self.btn_close.clicked.connect(self.close)

        # Barra de status
        self.status = QStatusBar(self)
        self.status.setGeometry(0, 450, 600, 10)
        self.status.showMessage("Pronto")

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(INI_PATH)

        self.fields["origem"].setText(config.get("Paths", "origem", fallback=""))
        self.fields["destino_simbolico"].setText(config.get("Paths", "destino_simbolico", fallback=""))
        self.fields["destino_juncoes"].setText(config.get("Paths", "destino_juncoes", fallback=""))
        self.fields["caminhovhdx"].setText(config.get("Paths", "caminhovhdx", fallback=""))

        self.fields["label"].setText(config.get("Config", "label", fallback=""))
        self.fields["icone"].setText(config.get("Config", "icone", fallback=""))

    def save_config(self):
        config = configparser.ConfigParser()
        config["Paths"] = {
            "origem": self.fields["origem"].text(),
            "destino_simbolico": self.fields["destino_simbolico"].text(),
            "destino_juncoes": self.fields["destino_juncoes"].text(),
            "caminhovhdx": self.fields["caminhovhdx"].text()
        }
        config["Config"] = {
            "label": self.fields["label"].text(),
            "icone": self.fields["icone"].text()
        }

        with open(INI_PATH, "w") as configfile:
            config.write(configfile)
        self.status.showMessage("Configuração salva com sucesso!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec())
