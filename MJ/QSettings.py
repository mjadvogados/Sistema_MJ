from PyQt6.QtWidgets import (
    QApplication, QWidget, QComboBox, QPushButton, QLabel
)
from PyQt6.QtCore import QSettings, Qt
import sys

class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciador de Servidor")
        self.setGeometry(100, 100, 300, 200)

        # --- QSettings
        self.settings = QSettings("FabianoSoft", "NetworkManager")

        # --- Label
        self.label = QLabel("Selecione o servidor:", self)
        self.label.setGeometry(50, 30, 200, 20)

        # --- ComboBox de servidores
        self.combo_servidor = QComboBox(self)
        self.combo_servidor.setGeometry(50, 60, 200, 30)
        self.combo_servidor.addItems(["Pelotas", "Rio Grande", "Santa Vitória"])
        self.combo_servidor.setStyleSheet("background-color: white; border-radius: 5px; padding: 2px;")

        # --- Restaurar última seleção
        last_server = self.settings.value("ultimo_servidor", "Pelotas")
        index = self.combo_servidor.findText(last_server, Qt.MatchFlag.MatchExactly)
        if index >= 0:
            self.combo_servidor.setCurrentIndex(index)

        # --- Botão Salvar
        self.btn_salvar = QPushButton("Salvar", self)
        self.btn_salvar.setGeometry(50, 110, 90, 30)
        self.btn_salvar.clicked.connect(self.salvar_configuracao)

        # --- Botão Fechar
        self.btn_fechar = QPushButton("Fechar", self)
        self.btn_fechar.setGeometry(160, 110, 90, 30)
        self.btn_fechar.clicked.connect(self.close)

    def salvar_configuracao(self):
        servidor = self.combo_servidor.currentText()
        self.settings.setValue("ultimo_servidor", servidor)
        self.setWindowTitle(f"Salvo: {servidor}")

    def closeEvent(self, event):
        # Salva ao fechar (opcional, já tem botão)
        self.settings.setValue("ultimo_servidor", self.combo_servidor.currentText())
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())
