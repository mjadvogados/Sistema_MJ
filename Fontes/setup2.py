import sys
from cx_Freeze import setup, Executable

# Dependências extras (se cx_Freeze não identificar automaticamente)
build_exe_options = {
    "packages": [],
    "include_files": [
        "Resources",        # Pasta a ser incluída
        "server2.ico"       # Ícone usado por ambos os executáveis
    ]
}

# Configurar ambos os executáveis
executables = [
    Executable(
        script="VHDX.py",
        base="Win32GUI",  # Se for GUI. Use "Console" se for terminal
        icon="server2.ico",
        target_name="VHDX.exe",
        uac_admin=True     # Solicita elevação de privilégios (UAC)
    ),
    Executable(
        script="NetworkSetup.py",
        base="Win32GUI",
        icon="server2.ico",
        target_name="NetworkSetup.exe",
        uac_admin=True
    )
]

setup(
    name="MySystemTools",
    version="1.0",
    description="Dois sistemas compilados em um só pacote",
    options={"build_exe": build_exe_options},
    executables=executables
)
