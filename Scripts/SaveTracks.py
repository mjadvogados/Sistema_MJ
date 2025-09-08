import time
import keyboard
import psutil
import win32gui
from plyer import notification

# Caminho do arquivo da playlist
playlist_path = "minha_playlist.txt"

def salvar_faixa(titulo):
    """Salva o título da faixa no arquivo da playlist."""
    with open(playlist_path, "a", encoding="utf-8") as f:
        f.write(titulo + "\n")
    mostrar_notificacao(titulo)

def mostrar_notificacao(titulo):
    """Exibe uma notificação informando que a faixa foi salva."""
    notification.notify(
        title="🎵 Faixa adicionada à Playlist",
        message=titulo,
        timeout=4
    )

def vlc_esta_rodando():
    """Verifica se o VLC está em execução."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and "vlc" in proc.info['name'].lower():
            return True
    return False

def obter_titulo_vlc():
    """Procura pela janela do VLC e retorna o título da faixa."""
    def callback(hwnd, titles):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "VLC media player" in title:
                titles.append(title)
        return True

    titulos = []
    win32gui.EnumWindows(callback, titulos)

    for titulo in titulos:
        faixa = titulo.replace(" - VLC media player", "").strip()
        if faixa:
            return faixa
    return None

def main():
    print("🎧 Monitorando VLC... Pressione Ctrl + Alt + K para salvar a faixa atual.")
    while True:
        try:
            if keyboard.is_pressed("ctrl+alt+k"):
                if vlc_esta_rodando():
                    faixa = obter_titulo_vlc()
                    if faixa:
                        salvar_faixa(faixa)
                        print(f"✅ Faixa salva: {faixa}")
                    else:
                        print("⚠️ Não foi possível obter o título da faixa.")
                else:
                    print("🚫 VLC não está em execução.")
                time.sleep(1.5)  # Evita múltiplos disparos
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n🛑 Encerrado pelo usuário.")
            break

if __name__ == "__main__":
    main()
