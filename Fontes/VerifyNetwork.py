import os
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

def verificar_caminhos():
    caminho_rede = r"\\servidor-pel\o$"
    unidade_mapeada = r"O:"

    caminho_rede_ok = os.path.exists(caminho_rede)
    unidade_mapeada_ok = os.path.exists(unidade_mapeada)

    if not caminho_rede_ok or not unidade_mapeada_ok:
        app = QApplication(sys.argv)

        mensagem = "Os seguintes caminhos não estão disponíveis:\n"
        if not caminho_rede_ok:
            mensagem += f"- {caminho_rede}\n"
        if not unidade_mapeada_ok:
            mensagem += f"- {unidade_mapeada}\n"

        QMessageBox.critical(None, "Erro de Conexão", mensagem)
        sys.exit(1)

if __name__ == "__main__":
    verificar_caminhos()
    print("Todos os caminhos estão disponíveis.")
