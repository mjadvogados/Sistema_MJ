from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton, QFrame
)
from PyQt6.QtGui import QPixmap, QFont, QPainterPath, QRegion
from PyQt6.QtCore import Qt, QRectF, QTimer
import sys
import os
import winsound  # 🎵 Importação da biblioteca de som (somente Windows)

dir_atual = os.path.dirname(os.path.abspath(sys.argv[0]))

class CustomMessageBox(QDialog):
    def __init__(
        self,
        icon_type,
        title_text,
        message_text,
        buttons_text,
        title_bg_color,
        title_text_color,
        window_bg_color,
        message_text_color,
        button_bg_color,
        button_text_color,
        border_color,
        window_width,
        window_height,
        title_font_size,
        message_font_size,
        button_font_size,
        timeout_duration=0
    ):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(window_width, window_height)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle(title_text)

        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

        self.button_clicked = None

        self.setup_ui(
            icon_type, title_text, message_text, buttons_text,
            title_bg_color, title_text_color, window_bg_color,
            message_text_color, button_bg_color, button_text_color,
            border_color, title_font_size, message_font_size, button_font_size
        )
        self.center_on_screen()

        if timeout_duration > 0:
            QTimer.singleShot(timeout_duration, self.accept)

    def setup_ui(
        self, icon_type, title_text, message_text, buttons_text,
        title_bg_color, title_text_color, window_bg_color,
        message_text_color, button_bg_color, button_text_color,
        border_color, title_font_size, message_font_size, button_font_size
    ):
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, self.width(), self.height())
        self.frame.setStyleSheet(f"""
            QFrame {{
                background-color: {window_bg_color};
                border-radius: 20px;
                border: 3px solid {border_color};
            }}
        """)

        self.title_label = QLabel(title_text, self.frame)
        self.title_label.setGeometry(15, 15, self.width() - 30, 30)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Segoe UI", title_font_size, QFont.Weight.Bold))
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {title_text_color};
                background-color: {title_bg_color};
                border-radius: 10px;
                padding: 4px;
            }}
        """)

        icon_file = f"{icon_type}.png"
        icon_path = os.path.join(dir_atual, "Resources", "Symbols", icon_file)
        pixmap = QPixmap(icon_path).scaled(
            128, 128,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.icon_label = QLabel(self.frame)
        self.icon_label.setGeometry(20, 60, 128, 128)
        self.icon_label.setPixmap(pixmap)

        # 🔊 Reproduzir som com base no tipo de ícone
        self.play_sound(icon_type)

        self.message_label = QLabel(message_text, self.frame)
        self.message_label.setGeometry(160, 60, self.width() - 180, 60)
        self.message_label.setFont(QFont("Segoe UI", message_font_size))
        self.message_label.setStyleSheet(f"color: {message_text_color};")
        self.message_label.setWordWrap(True)

        valid_buttons = [text for text in buttons_text if text.strip()]
        total_buttons = len(valid_buttons)

        if total_buttons > 0:
            button_width = 120
            spacing = 20
            total_width = total_buttons * button_width + (total_buttons - 1) * spacing
            start_x = (self.width() - total_width) // 2

            for i, text in enumerate(valid_buttons):
                btn = QPushButton(text, self.frame)
                btn.setGeometry(start_x + i * (button_width + spacing), self.height() - 60, button_width, 30)
                btn.setFont(QFont("Segoe UI", button_font_size, QFont.Weight.Bold))
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {button_bg_color};
                        color: {button_text_color};
                        border-radius: 15px;
                        border: 1px solid {border_color};
                    }}
                    QPushButton:hover {{
                        background-color: #0050ff;
                    }}
                    QPushButton:pressed {{
                        background-color: #001F3F;
                        padding-left: 2px;
                        padding-top: 2px;
                    }}
                """)
                btn.clicked.connect(lambda _, b=text: self.handle_button_click(b))

    def play_sound(self, icon_type):
        # 🔔 Mapeamento de sons padrão do Windows
        sounds = {
            "Critical": winsound.MB_ICONHAND,
            "Warning": winsound.MB_ICONEXCLAMATION,
            "Information": winsound.MB_ICONASTERISK,
            "Question": winsound.MB_ICONQUESTION
        }
        sound_flag = sounds.get(icon_type, winsound.MB_OK)
        winsound.MessageBeep(sound_flag)

    def handle_button_click(self, text):
        self.button_clicked = text
        self.accept()

    def center_on_screen(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        center_point = screen_geometry.center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

def showMessageBox(
    icon_type,
    title_text,
    message_text,
    buttons_text,
    title_bg_color="red",
    title_text_color="white",
    window_bg_color="orange",
    message_text_color="white",
    button_bg_color="blue",
    button_text_color="white",
    border_color="red",
    window_width=500,
    window_height=200,
    title_font_size=14,
    message_font_size=13,
    button_font_size=12,
    timeout_duration=0
):
    box = CustomMessageBox(
        icon_type,
        title_text,
        message_text,
        buttons_text,
        title_bg_color,
        title_text_color,
        window_bg_color,
        message_text_color,
        button_bg_color,
        button_text_color,
        border_color,
        window_width,
        window_height,
        title_font_size,
        message_font_size,
        button_font_size,
        timeout_duration
    )
    box.exec()
    return box.button_clicked

# 🧪 Exemplo de uso
if __name__ == "__main__":
    app = QApplication(sys.argv)

    resposta = showMessageBox(
        icon_type="Information",
        title_text="MJ Advogados - Servidor Pronto!",
        message_text="Unidade X: conectada com sucesso!",
        buttons_text=["OK", "Cancelar"],
        timeout_duration=15000
    )

    print(f"Botão pressionado: {resposta}")
