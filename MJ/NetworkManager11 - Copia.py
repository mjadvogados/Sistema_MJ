import sys
import os
import tempfile
from PyQt6.QtWidgets import QMainWindow, QFrame, QPushButton, QCheckBox, QStatusBar, QApplication
from PyQt6.QtCore import Qt, QCoreApplication, QTimer, QThread, QObject, pyqtSignal
from pathlib import Path
import re
import threading
import winsound
from FilesUtils import set_attrib, run_hidden, clear_target, openX, diskO
from SaveServer import load_config, save_config
from Parameters import load_parameters
from SelectServer2 import SetServer

# Carregar parâmetros do arquivo .ini
network_drive, server_drive, source, symbolic, junctions, label, folders_ignored = load_parameters()

# Preencher as variáveis conforme solicitado
origem = source
destino_simbolico = symbolic
destino_juncoes = junctions
pastas_ignoradas = folders_ignored
labelX = label


# Função auxiliar para obter caminho do som
def obter_caminho_som(nome_arquivo):
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    caminho_relativo = os.path.join(base_dir, "Resources", "Sounds", nome_arquivo)
    caminho_absoluto = os.path.join(r"C:\MJ-Network\Resources\Sounds", nome_arquivo)
    return caminho_relativo if os.path.exists(caminho_relativo) else caminho_absoluto


# Função para obter usuário logado a partir de um arquivo temporário
def obter_usuario_logado():
    try:
        caminho_arquivo = os.path.join(tempfile.gettempdir(), "userlog.dat")
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return None
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


# --- Worker para rodar a criação de junções em segundo plano ---
class Worker(QObject):
    finished = pyqtSignal()

    def __init__(self, pastas):
        super().__init__()
        self.pastas = pastas

    def run(self):
        criar_juncoes(self.pastas)
        self.finished.emit()


# --- Janela principal ---
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

        # Obter o usuário logado
        usuario_logado = obter_usuario_logado()
        print(usuario_logado)

        # Se não for a Graciele, remover as pastas restritas
        if usuario_logado not in ["Graciele", "Admin", "João"]:
            pastas = [p for p in pastas if p not in ["08 - Financeiro", "09 - Graciele"]]

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

        if not selecionadas:
            self.status.showMessage("Nenhuma pasta selecionada. Junções removidas.")
            return

        # 🔊 Iniciar som em loop numa thread separada
        self.som_thread = threading.Thread(target=self.tocar_som, daemon=True)
        self.som_thread.start()

        # 🧵 Criar thread e worker
        self.thread = QThread()
        self.worker = Worker(selecionadas)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.finalizar_aplicacao)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def tocar_som(self):
        caminho = obter_caminho_som("wait.wav")
        winsound.PlaySound(caminho, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

    def parar_som(self):
        winsound.PlaySound(None, winsound.SND_PURGE)

    def finalizar_aplicacao(self):
        self.parar_som()
        save_config(os.getlogin(), [cb.text() for cb in self.checkboxes if cb.isChecked()])
        openX(self)
        self.status.showMessage("Junções aplicadas com sucesso e unidade X: aberta!")

        QTimer.singleShot(300, self.close)
        QTimer.singleShot(600, QCoreApplication.quit)


def start_main_window():
    window = FolderSelectorWindow()
    window.show()
    return window


# Execução principal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = start_main_window()
    sys.exit(app.exec())
