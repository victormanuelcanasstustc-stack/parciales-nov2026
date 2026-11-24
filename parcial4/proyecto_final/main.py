import json
from pathlib import Path

from converter import (
    cargar_tasas_csv,
    convertir_monto,
    obtener_tasas_api,
)
from utils import formatear_monto, parsear_monto


DIRECTORIO_PROYECTO = Path(__file__).resolve().parent


def cargar_configuracion():
    """Lee la configuración privada del proyecto."""
    ruta = DIRECTORIO_PROYECTO / "config.json"

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def ejecutar_conversor():
    """Coordina las entradas, la consulta de tasas y la presentación."""
    print("===================================")
    print("       CONVERSOR DE DIVISAS")
    print("===================================")

    try:
        configuracion = cargar_configuracion()
        monto_texto = input("Ingrese el monto que desea convertir: ")
        monto = parsear_monto(monto_texto)

        moneda_origen = input(
            "Moneda de origen (USD, EUR, COP): "
        ).strip().upper()
        moneda_destino = input(
            "Moneda de destino (USD, EUR, COP): "
        ).strip().upper()

        tasas = obtener_tasas_api(
            configuracion["api_url"],
            configuracion["api_key"],
            moneda_origen,
        )

        if tasas is None:
            print("Se utilizarán las tasas locales de respaldo.")
            ruta_csv = DIRECTORIO_PROYECTO / "datos" / "tasas.csv"
            tasas = cargar_tasas_csv(ruta_csv, moneda_origen)
        else:
            print("Tasas obtenidas desde el servicio externo.")

        resultado = convertir_monto(
            monto,
            moneda_origen,
            moneda_destino,
            tasas,
        )

        tasa_aplicada = (
            1.0
            if moneda_origen == moneda_destino
            else float(tasas[moneda_destino])
        )

        print("-----------------------------------")
        print("RESUMEN DE LA CONVERSIÓN")
        print("Monto original:", formatear_monto(monto), moneda_origen)
        print("Tasa aplicada:", tasa_aplicada)
        print(
            "Resultado:",
            formatear_monto(resultado),
            moneda_destino,
        )
        print("-----------------------------------")

    except FileNotFoundError:
        print("Error: no se encontró config.json.")
        print("Crea el archivo a partir de config.example.json.")
    except (KeyError, OSError, ValueError) as error:
        print("No se pudo completar la conversión:", error)
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")

    print("Gracias por utilizar el conversor.")


def main():
    """Punto de entrada del programa."""
    ejecutar_conversor()


if __name__ == "__main__":
    main()
