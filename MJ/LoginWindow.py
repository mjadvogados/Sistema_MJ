import sys
import os
import tempfile
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QApplication, QComboBox
from PyQt6.QtCore import Qt, QRect, QCoreApplication
from PyQt6.QtGui import QFont
from Version import __version__
app_version = __version__


# ⚠️ Usuários válidos. Substitua por uma lógica segura em produção!
VALID_CREDENTIALS = {
    "Admin": "@1245@",
    "Fabiano": "@2123@",
    "João": "@joao0208@",
    "Graciele": "Graci3003@",
    "MJ": "mj1213mj"
}


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Login - MJ Advogados - V. {app_version}")
        self.setFixedSize(400, 250)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #FF8C8C; /* vermelho claro */
                border-radius: 15px;
            }
        """)

        self.centralizar_na_tela()

        # QFrame laranja
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 400, 250)
        self.frame.setStyleSheet("background-color: orange; border-radius: 15px;")

        # Estilos comuns
        label_font = QFont()
        label_font.setBold(True)
        label_font.setPointSize(10)

        input_font = QFont()
        input_font.setPointSize(10)
        input_font.setBold(False)

        # Label Usuário
        self.label_user = QLabel("Usuário:", self.frame)
        self.label_user.setFont(label_font)
        self.label_user.setStyleSheet("color: black;")
        self.label_user.setGeometry(20, 30, 200, 20)

        # ComboBox Usuário (substituindo QLineEdit)
        self.combo_user = QComboBox(self.frame)
        self.combo_user.setFont(input_font)
        self.combo_user.setStyleSheet("background-color: white; color: #00008B;")
        self.combo_user.setGeometry(20, 55, 250, 25)
        self.combo_user.addItems(VALID_CREDENTIALS.keys())

        # Label Senha
        self.label_pass = QLabel("Senha:", self.frame)
        self.label_pass.setFont(label_font)
        self.label_pass.setStyleSheet("color: black;")
        self.label_pass.setGeometry(20, 90, 200, 20)

        # Campo Senha
        self.input_pass = QLineEdit(self.frame)
        self.input_pass.setFont(input_font)
        self.input_pass.setStyleSheet("background-color: white; color: #00008B;")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setGeometry(20, 115, 250, 25)

        # Botão Login
        self.login_button = QPushButton("&Login", self.frame)
        self.login_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #002366; /* azul escuro */
                color: white;
                border-radius: 8px;
                padding: 6px 12px;
                border: 2px outset #001a4d; /* efeito 3D */
            }
            QPushButton:pressed {
                background-color: #001a4d;
                border-style: inset;
            }
        """)
        self.login_button.setGeometry(90, 170, 100, 35)
        self.login_button.clicked.connect(self.validar_login)
        self.input_pass.returnPressed.connect(self.login_button.click)

        # Botão Cancelar
        self.cancel_button = QPushButton("&Cancelar", self.frame)
        self.cancel_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #002366;
                color: white;
                border-radius: 8px;
                padding: 6px 12px;
                border: 2px outset #001a4d;
            }
            QPushButton:pressed {
                background-color: #001a4d;
                border-style: inset;
            }
        """)
        self.cancel_button.setGeometry(210, 170, 100, 35)
        self.cancel_button.clicked.connect(self.reject)

    def centralizar_na_tela(self):
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        x = (geometry.width() - self.width()) // 2
        y = (geometry.height() - self.height()) // 2
        self.move(x, y)

    def validar_login(self):
        usuario = self.combo_user.currentText()
        senha = self.input_pass.text()

        if VALID_CREDENTIALS.get(usuario) == senha:
            # Salvar o nome do usuário em arquivo userlog.dat na pasta temp
            temp_path = os.path.join(tempfile.gettempdir(), "userlog.dat")
            try:
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(usuario)
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao salvar usuário: {str(e)}")
                return
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.exec()
