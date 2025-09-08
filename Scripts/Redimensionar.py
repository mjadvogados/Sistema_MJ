import os
from PIL import Image

# 📁 Pasta com as imagens originais
pasta_origem = "imagens"
# 📁 Pasta onde as imagens redimensionadas serão salvas
pasta_destino = os.path.join(pasta_origem, "redimensionadas")

# 🛠️ Cria a pasta de destino se não existir
os.makedirs(pasta_destino, exist_ok=True)

# 🔁 Percorre todos os arquivos .png na pasta
for nome_arquivo in os.listdir(pasta_origem):
    if nome_arquivo.lower().endswith(".png"):
        caminho_origem = os.path.join(pasta_origem, nome_arquivo)
        caminho_destino = os.path.join(pasta_destino, nome_arquivo)

        # 📥 Abre a imagem
        imagem = Image.open(caminho_origem)

        # 📏 Redimensiona para 128x128
        imagem_redimensionada = imagem.resize((128, 128), Image.ANTIALIAS)

        # 💾 Salva na pasta de destino
        imagem_redimensionada.save(caminho_destino)

print("✅ Imagens redimensionadas com sucesso!")
