import os
import subprocess

def is_drive_mounted(drive_letter):
    return os.path.exists(f"{drive_letter}:\\")

def dismount_vhd_diskpart():
    if is_drive_mounted('X'):
        script = 'select vdisk file="C:\\Network\\Network.vhdx"\ndetach vdisk\n'
        subprocess.run(
            ["diskpart"],
            input=script.encode("utf-8"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

dismount_vhd_diskpart()
