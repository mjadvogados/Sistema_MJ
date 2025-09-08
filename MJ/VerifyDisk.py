import os
import ctypes
import sys

def unidade_existe(drive_letter="O:"):
    """Verifica se a unidade de rede está acessível."""
    return os.path.exists(drive_letter + "\\")

def main():
    if not unidade_existe("O:"):
        try:
            from ServerSelector import run_server
            run_server()
        except ImportError:
            print("Erro: Não foi possível importar a função 'run_server' do módulo SelectServer.")
        except Exception as e:
            print(f"Ocorreu um erro ao executar 'run_server': {e}")
    else:
        print("A unidade O: já está mapeada.")

if __name__ == "__main__":
    main()
