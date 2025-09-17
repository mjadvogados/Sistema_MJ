import winreg

def ocultar_unidades():
    chave = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
    valor_ocultar = 0x0000C003  # A, B, O, P

    try:
        # Abre a chave com permissões de escrita
        reg_key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, chave, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, "NoDrives", 0, winreg.REG_DWORD, valor_ocultar)
        winreg.CloseKey(reg_key)
        print("Unidades ocultadas com sucesso!")
    except Exception as e:
        print(f"Erro ao modificar o Registro: {e}")

ocultar_unidades()
