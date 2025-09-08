import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collections import deque
from threading import Timer

CAMINHO_MONITORADO = r"C:\Backups"

# Configuração do log
logging.basicConfig(
    filename="backup_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

event_cache = deque(maxlen=100)
pastas_renomeadas = set()
path_tipo_cache = {}  # Novo cache: {caminho: "Pasta" ou "Arquivo"}

def registrar_evento(evento):
    if evento not in event_cache:
        logging.info(evento)
        event_cache.append(evento)

def verificar_existencia_post_evento(path, acao, delay=0.5):
    def verificar():
        tipo = path_tipo_cache.get(path, "Arquivo")  # Assume "Arquivo" se não souber
        if not os.path.exists(path):
            registrar_evento(f"{tipo} {acao}: {path}")
    Timer(delay, verificar).start()

class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        tipo = "Pasta" if event.is_directory else "Arquivo"
        path_tipo_cache[event.src_path] = tipo

        if tipo == "Pasta" and os.path.basename(event.src_path).lower() == "nova pasta":
            return
        
        registrar_evento(f"{tipo} criado: {event.src_path}")

    def on_modified(self, event):
        tipo = "Pasta" if event.is_directory else "Arquivo"
        path_tipo_cache[event.src_path] = tipo
        registrar_evento(f"{tipo} modificado: {event.src_path}")

    def on_deleted(self, event):
        tipo = path_tipo_cache.get(event.src_path, "Arquivo")
        verificar_existencia_post_evento(event.src_path, "excluído")

    def on_moved(self, event):
        tipo = "Pasta" if event.is_directory else "Arquivo"
        path_tipo_cache[event.dest_path] = tipo
        if event.src_path in path_tipo_cache:
            del path_tipo_cache[event.src_path]

        if tipo == "Pasta":
            pastas_renomeadas.add(event.src_path)

        registrar_evento(f"{tipo} renomeado de: {event.src_path} para: {event.dest_path}")

if __name__ == "__main__":
    observer = Observer()
    handler = MonitorHandler()
    observer.schedule(handler, path=CAMINHO_MONITORADO, recursive=True)

    try:
        observer.start()
        print(f"Monitorando a pasta: {CAMINHO_MONITORADO}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
