from cx_Freeze import setup, Executable
import os

# Caminho para o ícone
icon_path = "server2.ico"

# Manifesto para solicitar elevação UAC
manifest = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>
'''

# Salva o manifesto como arquivo temporário
with open("uac.manifest", "w") as f:
    f.write(manifest)

# Configuração do executável
executables = [
    Executable(
        script="NetworkSetup.py",
        base="Win32GUI",  # Use "Console" se for app de terminal
        icon=icon_path,
        target_name="NetworkSetup.exe",
        manifest="uac.manifest"
    )
]

# Arquivos adicionais
include_files = [("Resources", "Resources")]

# Setup
setup(
    name="NetworkSetup Compiler",
    version="1.0",
    description="Compilador de VHDX com elevação UAC",
    options={
        "build_exe": {
            "include_files": include_files,
            "packages": [],
            "excludes": [],
        }
    },
    executables=executables
)
