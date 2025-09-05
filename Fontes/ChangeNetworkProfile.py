import winreg

def renomear_perfil_rede(nome_antigo, nome_novo):
    chave_base = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles"

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, chave_base, 0, winreg.KEY_READ | winreg.KEY_WRITE) as chave:
            for i in range(0, winreg.QueryInfoKey(chave)[0]):
                subchave_nome = winreg.EnumKey(chave, i)
                with winreg.OpenKey(chave, subchave_nome, 0, winreg.KEY_READ | winreg.KEY_WRITE) as subchave:
                    try:
                        valor_atual, tipo = winreg.QueryValueEx(subchave, "ProfileName")
                        if valor_atual == nome_antigo:
                            winreg.SetValueEx(subchave, "ProfileName", 0, tipo, nome_novo)
                            print(f"Perfil '{nome_antigo}' renomeado para '{nome_novo}' com sucesso.")
                            return
                    except FileNotFoundError:
                        continue
        print(f"Perfil com nome '{nome_antigo}' não encontrado.")
    except PermissionError:
        print("Permissão negada. Execute o script como administrador.")

# Exemplo de uso
renomear_perfil_rede("Hamachi", "📶")

