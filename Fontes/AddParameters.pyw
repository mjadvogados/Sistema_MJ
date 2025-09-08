import sys
import os
import configparser
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFrame, QLabel, QLineEdit,
    QPushButton, QPlainTextEdit, QStatusBar
)
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtCore import Qt, QEvent

# Caminho do arquivo .ini usando Path
folder_NetworkManager = Path(os.getenv("ProgramData")) / "NetworkManager"

# Cria a pasta se não existir
folder_NetworkManager.mkdir(parents=True, exist_ok=True)

# Caminho completo do arquivo .ini
arquivo_config = folder_NetworkManager / "ConfigProgram.ini"


class CustomPlainTextEdit(QPlainTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Tab:
            self.focusNextChild()  # Move para o próximo widget
        else:
            super().keyPressEvent(event)


class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MJ Advogados - Cadastro de Parâmetros")
        self.setFixedSize(600, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.centralizar_janela()
        self.setStyleSheet("border: 2px solid lightcoral; border-radius: 15px;")

        self.init_ui()

    def centralizar_janela(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        center_point = screen_geometry.center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def init_ui(self):
        # Fundo principal (QFrame)
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 600, 500)
        self.frame.setStyleSheet("background-color: orange; border-radius: 15px;")

        # Barra de título personalizada
        self.title_bar = QLabel("  MJ Advogados - Cadastro de Parâmetros", self.frame)
        self.title_bar.setGeometry(0, 0, 600, 40)
        self.title_bar.setStyleSheet("background-color: darkred; color: white; font-weight: bold;")
        self.title_bar.setFont(QFont("Arial", 12))
        self.title_bar.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        # Campos e etiquetas
        campos = [
            ("network_drive", "Unidade de Rede"),
            ("server_drive", "Unidade Servidor"),
            ("source", "Origem"),
            ("symbolic", "Destino Simbólico"),
            ("junctions", "Destino Junções"),
            ("label", "Label")
        ]

        self.inputs = {}
        top = 60

        for key, label_text in campos:
            label = QLabel(label_text, self.frame)
            label.setGeometry(20, top, 300, 20)
            label.setFont(QFont("Arial", 10))
            label.setAccessibleName(f"etiqueta_{key}")
            label.setAccessibleDescription(f"Etiqueta para o campo {label_text}")

            campo = QLineEdit(self.frame)
            campo.setGeometry(20, top + 20, 560, 25)
            campo.setAccessibleName(f"{key}")
            #campo.setAccessibleDescription(f"{label_text}")
            self.inputs[key] = campo

            top += 60

        # Campo de pastas ignoradas
        self.label_folders = QLabel("Pastas a Ignorar (uma por linha)", self.frame)
        self.label_folders.setGeometry(20, top, 300, 20)
        self.label_folders.setFont(QFont("Arial", 10))
        self.label_folders.setAccessibleName("etiqueta_folders_ignored")
        self.label_folders.setAccessibleDescription("Etiqueta para o campo de pastas a ignorar")

        self.folders_edit = CustomPlainTextEdit(self.frame)
        self.folders_edit.setGeometry(20, top + 20, 560, 80)
        self.folders_edit.setAccessibleName("folders_ignored")
        #self.folders_edit.setAccessibleDescription("Campo de entrada para pastas a serem ignoradas")
        self.folders_edit.setTabChangesFocus(True)  # Alternativa adicional

        top += 120

        # Botões
        self.btn_salvar = QPushButton("Salvar", self.frame)
        self.btn_salvar.setGeometry(180, top, 100, 35)
        self.btn_salvar.setStyleSheet("""
            QPushButton {
                background-color: navy;
                color: white;
                font-weight: bold;
                border-radius: 10px;
            }
        """)
        #self.btn_salvar.setAccessibleName("botao_salvar")
        #self.btn_salvar.setAccessibleDescription("Botão para salvar os dados")
        self.btn_salvar.clicked.connect(self.salvar)

        self.btn_fechar = QPushButton("Fechar", self.frame)
        self.btn_fechar.setGeometry(320, top, 100, 35)
        self.btn_fechar.setStyleSheet("""
            QPushButton {
                background-color: navy;
                color: white;
                font-weight: bold;
                border-radius: 10px;
            }
        """)
        #self.btn_fechar.setAccessibleName("botao_fechar")
        #self.btn_fechar.setAccessibleDescription("Botão para fechar a janela")
        self.btn_fechar.clicked.connect(self.close)

        # Barra de status
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.setStyleSheet("background-color: yellow; color: black; font-weight: bold;")
        self.status.showMessage("© 2025 - Fabiano Fonseca")

        # Carrega valores do .ini, se existir
        self.carregar_dados()

    def salvar(self):
        #folder_NetworkManager.mkdir(parents=True, exist_ok=True)
        config = configparser.ConfigParser()

        folders_list = self.folders_edit.toPlainText().splitlines()
        folders_set = set(filter(None, map(str.strip, folders_list)))

        config['Parameters'] = {
            'network_drive': self.inputs['network_drive'].text(),
            'server_drive': self.inputs['server_drive'].text(),
            'source': self.inputs['source'].text(),
            'symbolic': self.inputs['symbolic'].text(),
            'junctions': self.inputs['junctions'].text(),
            'label': self.inputs['label'].text(),
            'folders_ignored': str(folders_set)
        }

        with open(arquivo_config, 'w') as configfile:
            config.write(configfile)

        self.status.showMessage("Parâmetros salvos com sucesso!")

    def carregar_dados(self):
        if not arquivo_config.exists():
            return

        config = configparser.ConfigParser()
        config.read(arquivo_config)

        parametros = config['Parameters']

        for key in self.inputs:
            self.inputs[key].setText(parametros.get(key, ""))

        # Carregar folders_ignored
        texto = parametros.get('folders_ignored', '{}')
        try:
            folders = eval(texto)
            if isinstance(folders, set):
                self.folders_edit.setPlainText('\n'.join(sorted(folders)))
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec())
