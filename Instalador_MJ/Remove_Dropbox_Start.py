import os
import winreg
import shutil

def remover_do_registro(nome_item):
    chaves = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run")
    ]

    for raiz, caminho in chaves:
        try:
            with winreg.OpenKey(raiz, caminho, 0, winreg.KEY_ALL_ACCESS) as chave:
                try:
                    winreg.DeleteValue(chave, nome_item)
                    print(f'Removido do registro: {nome_item}')
                except FileNotFoundError:
                    pass  # O valor não existe
        except PermissionError:
            print(f"⚠️ Permissão negada para modificar: {caminho}")

def remover_da_pasta_startup(nome_item):
    pasta_startup = os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup')
    caminhos_possiveis = [
        os.path.join(pasta_startup, f"{nome_item}.lnk"),
        os.path.join(pasta_startup, f"{nome_item}.bat"),
        os.path.join(pasta_startup, f"{nome_item}.cmd")
    ]

    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            try:
                os.remove(caminho)
                print(f'Removido da pasta Startup: {os.path.basename(caminho)}')
            except Exception as e:
                print(f"Erro ao remover {caminho}: {e}")

def remover_dropbox_da_inicializacao():
    itens = ["DropboxStart", "Dropbox"]
    for item in itens:
        remover_do_registro(item)
        remover_da_pasta_startup(item)

if __name__ == "__main__":
    remover_dropbox_da_inicializacao()
