from pathlib import Path
from collections import Counter
import sys

carpeta = Path(
    sys.argv[1] if len(sys.argv) > 1
    else "parcial1/archivos_prueba"
)

if not carpeta.exists() or not carpeta.is_dir():
    raise SystemExit(f"Error: la carpeta no existe: {carpeta}")

conteo = Counter()

for archivo in carpeta.rglob("*"):
    if archivo.is_file():
        extension = archivo.suffix.lower() or "(sin extension)"
        conteo[extension] += 1

print(f"Conteo de archivos por extension en: {carpeta}")
print("-" * 45)

for extension, cantidad in sorted(conteo.items()):
    print(f"{extension:20} {cantidad:>5}")

print("-" * 45)
print(f"Total de archivos: {sum(conteo.values())}")
