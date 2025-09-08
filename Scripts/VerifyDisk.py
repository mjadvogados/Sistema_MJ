import os

def verificar_disco(letra_unidade):
    caminho = f"{letra_unidade.upper()}:\\"
    return os.path.isdir(caminho)

print(verificar_disco("s"))