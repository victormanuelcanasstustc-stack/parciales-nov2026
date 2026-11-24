import csv
import re
import sys

if len(sys.argv) != 2:
    print("Uso: python parcial3/contar_afectadas.py archivo.csv")
    sys.exit(1)

archivo = sys.argv[1]

patron = re.compile(r"^-?\d{1,3}(?:\.\d{3})+,\d{2}$")

afectadas = 0

with open(archivo, "r", encoding="utf-8-sig", newline="") as f:
    lector = csv.DictReader(f)

    if not lector.fieldnames or "monto" not in lector.fieldnames:
        raise ValueError("El CSV debe contener una columna llamada monto")

    for fila in lector:
        valor = (fila["monto"] or "").strip()

        if patron.fullmatch(valor):
            afectadas += 1

print(f"Filas con formato europeo: {afectadas}")
