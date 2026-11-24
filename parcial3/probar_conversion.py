import logging
from conversion import convertir

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s %(message)s | evento=%(evento)s | valor=%(valor)s",
)

casos = [
    ({"monto": "250.50"}, 250.50),
    ({"monto": "1,250.50"}, 1250.50),
    ({"monto": "1.250,00"}, 1250.00),
    ({"monto": "-3.000,25"}, -3000.25),
]

for fila, esperado in casos:
    resultado = convertir(fila)
    assert resultado == esperado
    print(f"Correcto: {fila['monto']} -> {resultado}")

try:
    convertir({"monto": "texto invalido"})
except ValueError as error:
    print(f"Error controlado correctamente: {error}")
else:
    raise AssertionError("Se esperaba un ValueError")

print("Todas las pruebas de conversión finalizaron correctamente.")
