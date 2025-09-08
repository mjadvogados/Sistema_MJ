from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout
)
from PyQt6.QtGui import QKeySequence,  QShortcut
from PyQt6.QtCore import Qt
import sys

class Formulario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Contato")
        self.setFixedSize(400, 250)
        self.init_ui()

    def init_ui(self):
        # --- Campos de entrada
        self.input_nome = QLineEdit()
        self.input_celular = QLineEdit()
        self.input_email = QLineEdit()
        self.input_whatsapp = QLineEdit()
        self.input_whatsapp.setReadOnly(True)
        self.input_whatsapp.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Sem parada de tabulação

        # --- Atalho F3 para focar no campo WhatsApp
        shortcut = QShortcut(QKeySequence("F3"), self)
        shortcut.activated.connect(lambda: self.input_whatsapp.setFocus())

        # --- Atualiza WhatsApp ao sair do campo celular
        self.input_celular.editingFinished.connect(self.atualizar_whatsapp)

        # --- Layout do formulário
        form_layout = QFormLayout()
        form_layout.addRow("Nome:", self.input_nome)
        form_layout.addRow("Celular:", self.input_celular)
        form_layout.addRow("e-Mail:", self.input_email)
        form_layout.addRow("WhatsApp:", self.input_whatsapp)

        # --- Botões
        btn_salvar = QPushButton("Salvar")
        btn_fechar = QPushButton("Fechar")
        btn_fechar.clicked.connect(self.close)

        # --- Layout dos botões centralizados
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_salvar)
        btn_layout.addWidget(btn_fechar)
        btn_layout.addStretch()

        # --- Layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def atualizar_whatsapp(self):
        celular = self.input_celular.text()
        self.input_whatsapp.setText(celular)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Formulario()
    window.show()
    sys.exit(app.exec())
