import winreg
import ctypes
import sys

def alternar_regedit():
    caminho = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
    valor_nome = "DisableRegistryTools"

    try:
        # Tenta abrir a chave existente
        chave = winreg.OpenKey(winreg.HKEY_CURRENT_USER, caminho, 0, winreg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        # Cria a chave se não existir
        chave = winreg.CreateKey(winreg.HKEY_CURRENT_USER, caminho)

    try:
        # Tenta ler o valor atual
        valor_atual, tipo = winreg.QueryValueEx(chave, valor_nome)
    except FileNotFoundError:
        # Se o valor não existir, assume como desbloqueado
        valor_atual = 0

    # Alterna o valor: 0 → 1 (bloquear), 1 → 0 (desbloquear)
    novo_valor = 0 if valor_atual == 1 else 1
    winreg.SetValueEx(chave, valor_nome, 0, winreg.REG_DWORD, novo_valor)
    winreg.CloseKey(chave)

    # Mensagem de status
    if novo_valor == 1:
        msg = "🔒 O acesso ao Regedit foi bloqueado para o usuário atual."
        titulo = "Bloqueio aplicado"
        icone = 0x40  # Ícone de informação
    else:
        msg = "✅ O acesso ao Regedit foi restaurado para o usuário atual."
        titulo = "Bloqueio removido"
        icone = 0x40

    ctypes.windll.user32.MessageBoxW(0, msg, titulo, icone)

alternar_regedit()
