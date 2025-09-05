import sys
import os
import tempfile
from PyQt6.QtWidgets import QMainWindow, QFrame, QPushButton, QCheckBox, QStatusBar, QApplication, QLabel, QComboBox, QLineEdit
from PyQt6.QtGui import QKeySequence,  QShortcut
from PyQt6.QtCore import Qt, QCoreApplication, QTimer, QThread, QObject, pyqtSignal
from pathlib import Path
import re
import threading
import time
import winsound
from FilesUtils import set_attrib, run_hidden, clear_target, openX, check_disk
from SaveServer import load_config, save_config, save_server, read_server
from Parameters import load_parameters
from CreateBat import create_bat
#from SelectServer2 import SetServer

def load_last_server():
    # Carregando o último servidor definido
    server_map = {
        r"\\servidor\o$": "Rio Grande",
        r"\\servidor-pel\o$": "Pelotas",
        r"\\servidor-svp\o$": "Santa Vitória"
    }

    # Busca no dicionário o ultimo servidor definido e recuperado pela função read_server()
    last_server_raw = read_server().lower()
    last_server = server_map.get(last_server_raw, "")

    return last_server



network_drive, server_drive, source, symbolic, junctions, label, folders_ignored = load_parameters()
origem = source
destino_simbolico = symbolic
destino_juncoes = junctions
pastas_ignoradas = folders_ignored
labelX = label


def obter_caminho_som(nome_arquivo):
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    caminho_relativo = os.path.join(base_dir, "Resources", "Sounds", nome_arquivo)
    caminho_absoluto = os.path.join(r"C:\MJ-Network\Resources\Sounds", nome_arquivo)
    return caminho_relativo if os.path.exists(caminho_relativo) else caminho_absoluto


def obter_usuario_logado():
    try:
        caminho_arquivo = os.path.join(tempfile.gettempdir(), "userlog.dat")
        with open(caminho_arquivo, "r") as f:
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


class Worker(QObject):
    finished = pyqtSignal()

    def __init__(self, pastas):
        super().__init__()
        self.pastas = pastas

    def run(self):
        criar_juncoes(self.pastas)
        self.finished.emit()


class FolderSelectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MJ Advogados - Seleção de Pastas")
        self.setFixedSize(600, 600)  # <-- Altura aumentada para 600
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        self.setStyleSheet("background-color: #ADD8E6;")

        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, self.width(), self.height())
        self.frame.setStyleSheet("QFrame { border: 3px solid #0000FF; border-radius: 15px; background-color: #ADD8E6; }")

        self.title_bar = QPushButton("MJ Advogados - Seleção de Pastas", self.frame)
        self.title_bar.setGeometry(0, 0, self.width(), 30)
        self.title_bar.setStyleSheet("QPushButton { background-color: #00008B; color: white; font-weight: bold; border: none; text-align: left; padding-left: 10px; }")
        self.title_bar.setEnabled(False)

        button_style = """
            QPushButton {
                background-color: #D3D3D3;
                color: black;
                font-weight: bold;
                border: 2px outset #A9A9A9;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:pressed {
                border: 2px inset #A9A9A9;
            }
        """

        # --- Nova Label "Selecionar Servidor"
        self.lbl_servidor = QLabel("Selecionar Servidor", self.frame)
        self.lbl_servidor.setGeometry(20, 40, 200, 25)
        self.lbl_servidor.setStyleSheet("font-weight: bold; color: black; background-color: lightblue;")

        self.lbl_ultimo = QLabel("Último Servidor", self.frame)
        self.lbl_ultimo.setGeometry(380, 40, 200, 25)
        self.lbl_ultimo.setStyleSheet("font-weight: bold; color: black; background-color: lightblue;")


        # --- ComboBox de servidores
        self.combo_servidor = QComboBox(self.frame)
        self.combo_servidor.setGeometry(20, 70, 200, 30)
        servidores = ["Pelotas", "Rio Grande", "Santa Vitória"]
        self.combo_servidor.addItems(servidores)
        self.combo_servidor.setStyleSheet("background-color: white; border-radius: 5px; padding: 2px;")
        self.combo_servidor.setAccessibleName("Selecionar Servidor")

        # Seleciona o último servidor, se estiver na lista
        if load_last_server() in servidores:
            index = servidores.index(load_last_server())
            self.combo_servidor.setCurrentIndex(index)
    
        # --- Botão ao lado da comboBox
        self.btn_aplicar_servidor = QPushButton("🖥 A&plicar", self.frame)
        self.btn_aplicar_servidor.setGeometry(230, 70, 100, 30)
        self.btn_aplicar_servidor.setStyleSheet(button_style)
        self.btn_aplicar_servidor.clicked.connect(self.selecionar_servidor)

        self.ql_ultimo = QLineEdit(self.frame)
        self.ql_ultimo.setGeometry(380, 70, 200, 30)
        # Remover parada de tabulação
        self.ql_ultimo.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # Estilo: fundo amarelo, texto preto em negrito
        self.ql_ultimo.setStyleSheet("background-color: yellow; color: black; font-weight: bold; border-radius: 5px; padding: 2px;")
        # Conteúdo do campo: valor da variável last_server
        self.ql_ultimo.setText(load_last_server())
        # Campo não editável
        self.ql_ultimo.setReadOnly(True)
        # Acessibilidade para leitores de tela no Windows
        self.ql_ultimo.setAccessibleName("Último servidor utilizado")
        #self.ql_ultimo.setAccessibleDescription("Campo de texto exibindo o último servidor acessado")

        # Adicionando tecla de atalho
        shortcut = QShortcut(QKeySequence("F3"), self)
        shortcut.activated.connect(lambda: self.ql_ultimo.setFocus())




        self.checkboxes = []

        # --- Botões Aplicar e Fechar (reposicionados na parte inferior)
        self.btn_aplicar = QPushButton("🔄 &Atualizar", self.frame)
        self.btn_aplicar.setGeometry(170, 540, 120, 35)
        self.btn_aplicar.setStyleSheet(button_style)
        self.btn_aplicar.clicked.connect(self.aplicar)

        self.btn_fechar = QPushButton("🚪 &Fechar", self.frame)
        self.btn_fechar.setGeometry(310, 540, 120, 35)
        self.btn_fechar.setStyleSheet(button_style)
        self.btn_fechar.clicked.connect(QCoreApplication.quit)

        self.status = QStatusBar(self)
        self.setStatusBar(self.status)
        self.status.setStyleSheet("QStatusBar { background-color: #006400; color: white; font-weight: bold; }")
        self.status.showMessage("© 2025 - Fabiano Fonseca")

        self.selecionar_pastas()





    def selecionar_pastas(self):
        print(origem)
        if not check_disk(origem):
            return
        
        try:
            pastas = [p for p in os.listdir(origem)
                      if os.path.isdir(os.path.join(origem, p)) and p not in pastas_ignoradas]
        except Exception:
            return

        usuario_logado = obter_usuario_logado()
        print(usuario_logado)

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
            cb.setGeometry(60, 120 + i * 25, 460, 25)
            cb.setChecked(pasta in selecionadas)
            cb.show()
            self.checkboxes.append(cb)

        self.status.showMessage(f"{len(pastas)} pastas carregadas da unidade O:.")

        self.setTabOrder(self.combo_servidor, self.btn_aplicar_servidor)
        for i in range(len(self.checkboxes) - 1):
            self        .setTabOrder(self.checkboxes[i], self.checkboxes[i + 1])
        self.setTabOrder(self.btn_aplicar_servidor, self.checkboxes[0])
        self.setTabOrder(self.checkboxes[-1], self.btn_aplicar)
        self.setTabOrder(self.btn_aplicar, self.btn_fechar)


    def aplicar(self):
        selecionadas = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        clear_target(destino_simbolico, destino_juncoes)

        if not selecionadas:
            self.status.showMessage("Nenhuma pasta selecionada. Junções removidas.")
            return

        self.som_thread = threading.Thread(target=self.tocar_som, daemon=True)
        self.som_thread.start()

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

    def selecionar_servidor(self):
        servidores = {
            "pelotas": r"\\servidor-pel\o$",
            "pelotas (backup)": r"\\pelotas-01\o$",
            "santa vitória": r"\\rg-13\o$",
            "rio grande": r"\\servidor\o$",
            "rio grande (backup)": r"\\rg-05\o$"
        }

        servidor = self.combo_servidor.currentText().lower()
        caminho = servidores.get(servidor, "")

        if not caminho:
            self.status.showMessage("Servidor inválido.")
            return

        save_server(caminho)
        create_bat(caminho)
        run_hidden(r"C:\MJ-Network\MJ.bat")
        # Atualiza o campo Último Servidor
        self.ql_ultimo.setText(load_last_server())

        # Esperar até 5 segundos pela unidade O:
        for _ in range(10):  # 10 tentativas de 0.5s = 5s
            if os.path.exists("O:"):
                #global origem  # <-- necessário para alterar a variável global
                #origem = "O:\\"  # <-- agora a variável aponta para a unidade mapeada
                self.status.showMessage(f"Servidor '{servidor}' aplicado com sucesso.")
                self.selecionar_pastas()
                return
            time.sleep(0.5)

        # Se depois das tentativas ainda não estiver acessível
        self.status.showMessage("Erro: unidade de rede não acessível.")



    def selecionar_servidor2(self):
        servidores = {
            "pelotas": r"\\servidor-pel\o$",
            "pelotas (backup)": r"\\pelotas-01\o$",
            "santa vitória": r"\\servidor-svp\o$",
            "rio grande": r"\\servidor\o$",
            "rio grande (backup)": r"\\rg-05\o$"
        }

        servidor = self.combo_servidor.currentText().lower()
        caminho = servidores.get(servidor, "")

        if not caminho:
            return

        
        save_server(caminho)
        create_bat(caminho)
        run_hidden(r"C:\MJ-Network\MJ.bat")
        self.selecionar_pastas()





def start_main_window():
    window = FolderSelectorWindow()
    window.show()
    return window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = start_main_window()
    sys.exit(app.exec())
