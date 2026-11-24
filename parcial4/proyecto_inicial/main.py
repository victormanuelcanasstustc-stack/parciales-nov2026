import json
import csv
import requests
from utils import validar_monto, formatear_monto

def main():
    print("===================================")
    print("       CONVERSOR DE DIVISAS")
    print("===================================")

    # Leer la configuración
    try:
        with open("config.json", "r", encoding="utf-8") as archivo:
            configuracion = json.load(archivo)
        api_key = configuracion["api_key"]
        api_url = configuracion["api_url"]
    except Exception as error:
        print("Error al leer la configuración:", error)
        return

    # Solicitar los datos al usuario
    try:
        monto_texto = input("Ingrese el monto que desea convertir: ")
        monto = float(monto_texto)

        if not validar_monto(monto):
            print("El monto debe ser mayor que cero.")
            return

        moneda_origen = input("Moneda de origen (USD, EUR, COP): ").upper()
        moneda_destino = input("Moneda de destino (USD, EUR, COP): ").upper()

        if moneda_origen not in ["USD", "EUR", "COP"]:
            print("La moneda de origen no está disponible.")
            return

        if moneda_destino not in ["USD", "EUR", "COP"]:
            print("La moneda de destino no está disponible.")
            return

        # Consultar las tasas del servicio externo
        tasas = {}
        respuesta_correcta = False

        try:
            encabezados = {"Authorization": "Bearer " + api_key}
            respuesta = requests.get(
                api_url,
                headers=encabezados,
                params={"base": moneda_origen},
                timeout=5
            )

            if respuesta.status_code == 200:
                datos_api = respuesta.json()
                tasas = datos_api["rates"]
                respuesta_correcta = True
                print("Tasas obtenidas desde el servicio externo.")
            else:
                print("El servicio externo no respondió correctamente.")

        except requests.exceptions.RequestException as error:
            print("No fue posible consultar el servicio externo:", error)
        except Exception as error:
            print("Ocurrió un error al procesar la respuesta:", error)

        # Utilizar el archivo CSV cuando la API no esté disponible
        if respuesta_correcta is False:
            print("Se utilizarán las tasas locales de respaldo.")
            try:
                with open("datos/tasas.csv", "r", encoding="utf-8") as archivo:
                    lector = csv.DictReader(archivo)
                    for fila in lector:
                        if fila["moneda_base"] == moneda_origen:
                            tasas[fila["moneda_destino"]] = float(fila["tasa"])
            except Exception as error:
                print("No se pudieron leer las tasas locales:", error)
                return

        # Obtener la tasa de conversión
        if moneda_origen == moneda_destino:
            tasa = 1.0
        else:
            try:
                tasa = float(tasas[moneda_destino])
            except Exception:
                print("No existe una tasa para esa conversión.")
                return

        # Calcular y presentar el resultado
        resultado = monto * tasa
        print("-----------------------------------")
        print("RESUMEN DE LA CONVERSIÓN")
        print("Monto original:", formatear_monto(monto), moneda_origen)
        print("Tasa aplicada:", tasa)
        print("Resultado:", formatear_monto(resultado), moneda_destino)
        print("-----------------------------------")

    except ValueError:
        print("Debe ingresar un número válido.")
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
    except Exception as error:
        print("Error inesperado:", error)

    print("Gracias por utilizar el conversor.")


if __name__ == "__main__":
    main()
