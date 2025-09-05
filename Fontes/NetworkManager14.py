# NetworkManager11.py

from PyQt6.QtWidgets import QMainWindow, QFrame, QPushButton, QCheckBox, QStatusBar, QApplication
from PyQt6.QtCore import Qt, QCoreApplication, QTimer
from pathlib import Path
import os
import re
from FilesUtils import set_attrib, run_hidden, clear_target, openX, diskO
from SaveServer import load_config, save_config
from Parameters import load_parameters
from SelectServer2 import SetServer  # Se precisar chamar, mas neste arquivo não vamos

#origem = r"O:"
#destino_simbolico = Path(r"X:\O")
#destino_juncoes = Path(r"X:")
#pastas_ignoradas = {"Imagens", "Documentos", "90 - Compartilhado", "99 - Backup-CPJ", ".dropbox.cache", "Vault", "Viagem de Balão"}

# Carregar parâmetros do arquivo .ini
network_drive, server_drive, source, symbolic, junctions, label, folders_ignored = load_parameters()

# Preencher as variáveis conforme solicitado
origem = source
destino_simbolico = symbolic
destino_juncoes = junctions
pastas_ignoradas = folders_ignored




def criar_juncoes(pastas):
    destino_simbolico.mkdir(parents=True, exist_ok=True)
    contador_sem_numero = 71
    padrao_numero = re.compile(r'^(\d{2})')

    for pasta in pastas:
        if pasta in pastas_ignoradas:
            continue

        caminho_origem = os.path.join(origem, pasta)
        if not os.path.isdir(caminho_origem):
            continue

        match = padrao_numero.match(pasta)
        if match:
            nome_link = match.group(1)
        else:
            if contador_sem_numero > 89:
                print(f'❌ Número máximo de pastas sem numeração excedido. Operação cancelada.')
                return
            nome_link = f'{contador_sem_numero:02d}'
            contador_sem_numero += 1

        link = destino_simbolico / nome_link
        juncao = destino_juncoes / pasta

        run_hidden(f'mklink /D "{link}" "{caminho_origem}"')
        run_hidden(f'mklink /J "{juncao}" "{link}"')

    set_attrib(destino_simbolico)

class FolderSelectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MJ Advogados - Seleção de Pastas")
        self.setFixedSize(600, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, self.width(), self.height())

        self.btn_selecionar = QPushButton("&Servidor", self.frame)
        self.btn_aplicar = QPushButton("&Aplicar", self.frame)
        self.btn_fechar = QPushButton("&Fechar", self.frame)

        self.btn_selecionar.setGeometry(20, 20, 120, 30)
        self.btn_aplicar.setGeometry(150, 20, 120, 30)
        self.btn_fechar.setGeometry(280, 20, 120, 30)

        self.btn_selecionar.clicked.connect(self.selecionar_servidor)
        self.btn_aplicar.clicked.connect(self.aplicar)
        self.btn_fechar.clicked.connect(QCoreApplication.quit)

        self.checkboxes = []

        self.status = QStatusBar(self)
        self.setStatusBar(self.status)
        self.status.showMessage("© 2025 - Fabiano Fonseca")

        self.selecionar_pastas()

    def selecionar_servidor(self):
        self.selecionarServidor = SetServer()
        self.selecionarServidor.show()
        self.selecionar_pastas()

    def selecionar_pastas(self):
        try:
            pastas = [p for p in os.listdir(origem)
                      if os.path.isdir(os.path.join(origem, p)) and p not in pastas_ignoradas]
        except Exception:
            return

        for cb in self.checkboxes:
            cb.hide()
            cb.setParent(None)
            cb.deleteLater()
        self.checkboxes.clear()

        _, selecionadas = load_config()
        for i, pasta in enumerate(sorted(pastas)):
            cb = QCheckBox(pasta, self.frame)
            cb.setGeometry(60, 70 + i * 25, 460, 25)
            cb.setChecked(pasta in selecionadas)
            cb.show()
            self.checkboxes.append(cb)

        self.status.showMessage(f"{len(pastas)} pastas carregadas da unidade O:.")

    def aplicar(self):
        selecionadas = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        clear_target(destino_simbolico, destino_juncoes)

        if selecionadas:
            criar_juncoes(selecionadas)
            save_config(os.getlogin(), selecionadas)

            # ✅ Mostra notificação e abre unidade X:
            openX(self)

            # ✅ Mensagem opcional de sucesso
            self.status.showMessage("Junções aplicadas com sucesso e unidade X: aberta!")

            # ✅ Encerra a janela principal após pequena espera (opcional)
            QTimer.singleShot(300, self.close)  # Fecha janela após 300 ms

            # ✅ Encerra toda a aplicação após mais um pequeno atraso
            QTimer.singleShot(600, QCoreApplication.quit)

        else:
            self.status.showMessage("Nenhuma pasta selecionada. Junções removidas.")



    def aplicar2(self):
        selecionadas = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        clear_target(destino_simbolico, destino_juncoes)

        if selecionadas:
            criar_juncoes(selecionadas)
            save_config(os.getlogin(), selecionadas)
            openX(self)
            self.status.showMessage("Junções aplicadas com sucesso e unidade X: aberta!")
        else:
            self.status.showMessage("Nenhuma pasta selecionada. Junções removidas.")

def start_main_window():
    window = FolderSelectorWindow()
    window.show()
    return window
