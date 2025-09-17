import os
import subprocess
import datetime
import winreg
import traceback

TERMO = "dropbox"
CHAVES_RAIZ = [
    (winreg.HKEY_CURRENT_USER, "HKEY_CURRENT_USER"),
    (winreg.HKEY_LOCAL_MACHINE, "HKEY_LOCAL_MACHINE")
]

def fazer_backup_registro():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_backup = f"backup_registro_{timestamp}.reg"
    print(f"🔁 Fazendo backup do registro em '{arquivo_backup}'...")

    try:
        with open(arquivo_backup, 'w') as f:
            pass  # Apenas para garantir que pode criar o arquivo

        # Backup completo
        comando = f'reg export HKLM HKLM_backup_{timestamp}.reg /y & reg export HKCU HKCU_backup_{timestamp}.reg /y'
        subprocess.run(comando, shell=True, check=True)
        print("✅ Backup concluído.")
    except Exception as e:
        print(f"❌ Falha ao criar backup: {e}")
        exit(1)

def remover_valores_com_dropbox(raiz, caminho_str):
    try:
        with winreg.OpenKey(raiz, caminho_str, 0, winreg.KEY_READ | winreg.KEY_WRITE) as chave:
            i = 0
            valores_para_remover = []
            while True:
                try:
                    nome, dados, tipo = winreg.EnumValue(chave, i)
                    if TERMO in nome.lower() or (isinstance(dados, str) and TERMO in dados.lower()):
                        valores_para_remover.append(nome)
                    i += 1
                except OSError:
                    break
            for nome in valores_para_remover:
                try:
                    winreg.DeleteValue(chave, nome)
                    print(f"[Valor] Removido: '{nome}' de {caminho_str}")
                except Exception as e:
                    print(f"Erro ao remover valor '{nome}' de {caminho_str}: {e}")
    except PermissionError:
        print(f"⚠️ Sem permissão: {caminho_str}")
    except FileNotFoundError:
        pass
    except Exception:
        traceback.print_exc()

def remover_chaves_com_dropbox(raiz, caminho_str):
    try:
        with winreg.OpenKey(raiz, caminho_str, 0, winreg.KEY_READ | winreg.KEY_WRITE) as chave:
            subchaves = []
            i = 0
            while True:
                try:
                    subchave = winreg.EnumKey(chave, i)
                    subchaves.append(subchave)
                    i += 1
                except OSError:
                    break

            for subchave in subchaves:
                subcaminho = f"{caminho_str}\\{subchave}"
                remover_chaves_com_dropbox(raiz, subcaminho)
                if TERMO in subchave.lower():
                    try:
                        winreg.DeleteKey(chave, subchave)
                        print(f"[Chave] Removida: {subcaminho}")
                    except Exception as e:
                        print(f"Erro ao remover chave {subcaminho}: {e}")
    except PermissionError:
        print(f"⚠️ Sem permissão para chave: {caminho_str}")
    except FileNotFoundError:
        pass
    except Exception:
        traceback.print_exc()

def percorrer_todas_chaves():
    for raiz, nome_raiz in CHAVES_RAIZ:
        print(f"\n🔍 Varrendo: {nome_raiz}")
        pilha = [""]
        while pilha:
            caminho_atual = pilha.pop()
            try:
                with winreg.OpenKey(raiz, caminho_atual, 0, winreg.KEY_READ) as chave:
                    remover_valores_com_dropbox(raiz, caminho_atual)
                    remover_chaves_com_dropbox(raiz, caminho_atual)

                    i = 0
                    while True:
                        try:
                            subchave = winreg.EnumKey(chave, i)
                            pilha.append(f"{caminho_atual}\\{subchave}" if caminho_atual else subchave)
                            i += 1
                        except OSError:
                            break
            except PermissionError:
                continue
            except FileNotFoundError:
                continue
            except Exception:
                traceback.print_exc()

if __name__ == "__main__":
    fazer_backup_registro()
    percorrer_todas_chaves()
    print("\n✅ Limpeza concluída.")
