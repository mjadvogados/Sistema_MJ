import subprocess
import datetime
import os

log_file = r"C:\rclone\mount_log.txt"
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def is_drive_mounted(drive_letter):
    import psutil
    return any(part.mountpoint.startswith(drive_letter) for part in psutil.disk_partitions())

if is_drive_mounted("P:"):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - Unidade P: já está montada. Nenhuma ação realizada.\n")
else:
    try:
        # Executa o rclone diretamente, sem shell, sem start, como processo independente
        subprocess.Popen([
            "rclone", "mount", "OneDrive:", "P:",
            "--vfs-cache-mode", "full",
            "--metadata",
            "--drive-use-trash=false",
            "--links"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} - Montagem do OneDrive iniciada com sucesso.\n")
    except Exception as e:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} - Erro ao iniciar montagem: {e}\n")
