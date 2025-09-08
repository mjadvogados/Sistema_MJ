#SingleInstance Force
#NoTrayIcon


; Oculta a unidade O:
RegWrite, REG_DWORD, HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer, NoDrives, 0x4000

; Define o rótulo como "Backup"
RunWait, label O: Backup, , Hide
