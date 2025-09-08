from PyQt6.QtWidgets import (
    QApplication, QWidget, QComboBox, QPushButton, QLabel
)
from PyQt6.QtCore import QSettings, Qt
import sys

class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciador de Servidor")
        self.setGeometry(100, 100, 320, 220)

        self.settings = QSettings("FabianoSoft", "GerenciadorDeRede")

        # --- Label Usuário
        self.label_usuario = QLabel("Usuário:", self)
        self.label_usuario.setGeometry(30, 30, 100, 20)

        # --- ComboBox de usuários
        self.combo_usuario = QComboBox(self)
        self.combo_usuario.setGeometry(120, 30, 160, 30)
        self.combo_usuario.addItems(["Fabiano", "João", "Maria", "Ana"])
        self.combo_usuario.setStyleSheet("background-color: white; border-radius: 5px; padding: 2px;")
        self.combo_usuario.currentTextChanged.connect(self.carregar_servidor_do_usuario)

        # --- Label Servidor
        self.label_servidor = QLabel("Servidor:", self)
        self.label_servidor.setGeometry(30, 80, 100, 20)

        # --- ComboBox de servidores
        self.combo_servidor = QComboBox(self)
        self.combo_servidor.setGeometry(120, 80, 160, 30)
        self.combo_servidor.addItems(["Pelotas", "Rio Grande", "Santa Vitória"])
        self.combo_servidor.setStyleSheet("background-color: white; border-radius: 5px; padding: 2px;")

        # --- Botão Salvar
        self.btn_salvar = QPushButton("💾 Salvar", self)
        self.btn_salvar.setGeometry(50, 140, 100, 30)
        self.btn_salvar.clicked.connect(self.salvar_configuracao)

        # --- Botão Fechar
        self.btn_fechar = QPushButton("🚪 Fechar", self)
        self.btn_fechar.setGeometry(170, 140, 100, 30)
        self.btn_fechar.clicked.connect(self.close)

        # --- Carregar servidor do usuário inicial
        self.carregar_servidor_do_usuario(self.combo_usuario.currentText())

    def carregar_servidor_do_usuario(self, usuario):
        chave = f"usuarios/{usuario}"
        servidor = self.settings.value(chave, "Pelotas")
        index = self.combo_servidor.findText(servidor, Qt.MatchFlag.MatchExactly)
        if index >= 0:
            self.combo_servidor.setCurrentIndex(index)

    def salvar_configuracao(self):
        usuario = self.combo_usuario.currentText()
        servidor = self.combo_servidor.currentText()
        chave = f"usuarios/{usuario}"
        self.settings.setValue(chave, servidor)
        self.setWindowTitle(f"{usuario} → {servidor} (salvo)")

    def closeEvent(self, event):
        self.salvar_configuracao()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())
        