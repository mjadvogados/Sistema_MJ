import sys
import os
from FilesUtils import check_disk
if not check_disk("o"):
    print("Disco disponível")
else:
    print("Disco não disponível")