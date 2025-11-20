import sys
from pathlib import Path

# añadir la carpeta micro_productores al sys.path para que "import application" funcione
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

