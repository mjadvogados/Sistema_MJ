# Parar todos os processos relacionados ao Dropbox
Get-Process -Name "Dropbox" -ErrorAction SilentlyContinue | Stop-Process -Force

# Remover diretórios e arquivos do Dropbox
Remove-Item "C:\Program Files (x86)\Dropbox" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Users\$env:USERNAME\AppData\Roaming\Dropbox" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Users\$env:USERNAME\AppData\Local\Dropbox" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Users\$env:USERNAME\Dropbox" -Recurse -Force -ErrorAction SilentlyContinue

# Limpar as entradas no registro
Remove-Item "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Dropbox" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Dropbox" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "HKCU:\Software\Dropbox" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "HKLM:\SOFTWARE\Dropbox" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Dropbox foi removido com sucesso!"
