@echo off
pyinstaller --noconfirm --onedir --windowed --icon=install.ico --add-data "Zips;Zips" --uac-admin Install.py
exit
