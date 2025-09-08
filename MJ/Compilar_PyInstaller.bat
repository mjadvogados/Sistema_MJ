@echo off
pyinstaller --noconfirm --onedir --windowed --icon=server2.ico --add-data "Resources;Resources" --uac-admin NetworkSetup.py
pyinstaller --noconfirm --onedir --windowed --icon=server2.ico --add-data "Resources;Resources" --uac-admin VHDX.py
pyinstaller --noconfirm --onedir --windowed --icon=mj.ico Servidor.py

