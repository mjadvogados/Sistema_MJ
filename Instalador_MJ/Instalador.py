import os
import shutil
import subprocess
from zipfile import ZipFile

# Define o caminho da pasta temporária e dos arquivos
temp_dir = os.getenv('TEMP')  # Diretório temporário do sistema
zip_file_path = os.path.join(temp_dir, 'Network-Pel.zip')
destination_dir = r'C:\Network'

# Função para verificar a existência de um arquivo
def file_exists(file_path):
    return os.path.exists(file_path)

# Função para deletar arquivos
def delete_file(file_path):
    if file_exists(file_path):
        os.remove(file_path)

# Função para criar diretório
def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Verifica e apaga o diretório de destino se existir
if file_exists(destination_dir):
    shutil.rmtree(destination_dir)  # Apaga a pasta e todo o conteúdo

# Cria o diretório de destino
create_dir(destination_dir)

# Verifica se o arquivo ZIP existe
if not file_exists(zip_file_path):
    print("Erro: O arquivo Network-Pel.zip não foi encontrado no diretório Temp!")
    exit(1)

# Descompacta o arquivo .zip na pasta de destino
try:
    with ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_dir)
    print(f"Arquivo extraído para {destination_dir}")
except Exception as e:
    print(f"Erro ao extrair o arquivo: {e}")
    exit(1)

# Verifica se o arquivo VHD foi extraído corretamente
vhdx_file_path = os.path.join(destination_dir, 'Network-Pel.vhdx')
if not file_exists(vhdx_file_path):
    print("Erro: O arquivo VHD não foi extraído corretamente!")
    exit(1)

# Define a pasta como oculta e do sistema (usando atributos via cmd)
subprocess.run(['cmd', '/c', f'attrib +h +s "{destination_dir}"'], check=True)

# Limpeza dos arquivos temporários
delete_file(zip_file_path)

# Mensagem de sucesso
print("A extração foi concluída com sucesso, a pasta foi ocultada e os arquivos temporários foram excluídos!")

