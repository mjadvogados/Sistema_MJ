$uninstallKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Dropbox"
$uninstallString = (Get-ItemProperty -Path $uninstallKey).UninstallString

if ($uninstallString) {
    Start-Process -FilePath $uninstallString -ArgumentList "/quiet", "/norestart" -Wait
} else {
    Write-Host "Não foi encontrado o Dropbox para desinstalar."
}
