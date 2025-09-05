import os
import sys
import subprocess
from FilesUtils import drive_label, hide_drive  # Certifique-se que essas funções estão funcionando

def run_hidden(cmd):
    """Executa um comando sem exibir janela e retorna o resultado completo do processo."""
    return subprocess.run(
        cmd,
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

def log_error(msg):
    """Grava mensagens de erro no arquivo de log."""
    with open("erros.log", "a", encoding="utf-8") as log_file:
        log_file.write(msg + "\n\n")

def map_drive(network_path, drive_letter, username="administrador", password="mj2145mj", label="Servidor"):
    """
    Mapeia e oculta uma unidade de rede no Windows.
    """
    try:
        # Remove conexões anteriores
        run_hidden('net use * /delete /yes')
        run_hidden(f'net use {drive_letter}: /delete /yes')

        # Tenta mapear a nova unidade
        result = run_hidden(f'net use {drive_letter}: "{network_path}" /user:{username} {password} /persistent:yes')

        if result.returncode != 0:
            log_error(f"[ERRO] Falha ao mapear {drive_letter}: para {network_path}")
            log_error(f"Código de Retorno: {result.returncode}")
            log_error(f"Erro: {result.stderr.strip()}")
        else:
            # Define o rótulo e oculta a unidade
            drive_label(f"{drive_letter}:\\", label)
            hide_drive(drive_letter)

    except Exception as e:
        log_error(f"[EXCEÇÃO] {str(e)}")
    finally:
        sys.exit(0)

# Execução
if __name__ == "__main__":
    map_drive(r"\\servidor\dropbox$", "L", label="Dropbox")
