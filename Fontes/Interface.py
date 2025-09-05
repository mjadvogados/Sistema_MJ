from PyQt6.QtGui import QPainterPath, QRegion
from PyQt6.QtCore import QRect

# Janela sem borda e com cantos arredondados
self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

# Fundo da janela em azul escuro
self.setStyleSheet("background-color: #00008B;")

# Criar máscara arredondada para a janela
path = QPainterPath()
path.addRoundedRect(QRect(0, 0, self.width(), self.height()), 15, 15)
region = QRegion(path.toFillPolygon().toPolygon())
self.setMask(region)

# Frame principal com borda azul e cantos arredondados
self.frame = QFrame(self)
self.frame.setGeometry(0, 0, self.width(), self.height())
self.frame.setStyleSheet("""
    QFrame {
        border: 3px solid #0000CD; /* Azul médio */
        border-radius: 15px;
        background-color: #00008B; /* Azul escuro */
    }
""")

# Barra de título com cantos arredondados
self.title_bar = QPushButton("MJ Advogados - Seleção de Pastas", self.frame)
self.title_bar.setGeometry(0, 0, self.width(), 30)
self.title_bar.setStyleSheet("""
    QPushButton {
        background-color: #000080; /* Azul marinho */
        color: white;
        font-weight: bold;
        border-radius: 15px;
        border: none;
        text-align: left;
        padding-left: 10px;
    }
""")
self.title_bar.setEnabled(False)

# Estilo dos botões: laranja com letras pretas, arredondados e com efeito 3D
button_style = """
    QPushButton {
        background-color: orange;
        color: black;
        font-weight: bold;
        border: 2px outset #A0522D;  /* efeito 3D - relevo */
        border-radius: 10px;
        padding: 5px;
    }
    QPushButton:pressed {
        border: 2px inset #A0522D;  /* efeito 3D - pressionado */
    }
"""
