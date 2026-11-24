import csv

import requests

from utils import MONEDAS_DISPONIBLES, validar_monto


def convertir_monto(monto, moneda_origen, moneda_destino, tasas):
    """Calcula una conversión sin leer entradas ni imprimir resultados."""
    if not validar_monto(monto):
        raise ValueError("El monto debe ser mayor que cero.")

    if moneda_origen not in MONEDAS_DISPONIBLES:
        raise ValueError("La moneda de origen no está disponible.")

    if moneda_destino not in MONEDAS_DISPONIBLES:
        raise ValueError("La moneda de destino no está disponible.")

    if moneda_origen == moneda_destino:
        tasa = 1.0
    else:
        try:
            tasa = float(tasas[moneda_destino])
        except (KeyError, TypeError, ValueError):
            raise ValueError("No existe una tasa para esa conversión.")

    return monto * tasa


def cargar_tasas_csv(ruta_csv, moneda_origen):
    """Lee del CSV las tasas correspondientes a la moneda de origen."""
    tasas = {}

    with open(ruta_csv, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            if fila["moneda_base"] == moneda_origen:
                tasas[fila["moneda_destino"]] = float(fila["tasa"])

    return tasas


def obtener_tasas_api(api_url, api_key, moneda_origen):
    """Consulta el servicio externo y devuelve sus tasas o None si falla."""
    encabezados = {"Authorization": "Bearer " + api_key}

    try:
        respuesta = requests.get(
            api_url,
            headers=encabezados,
            params={"base": moneda_origen},
            timeout=5,
        )
        respuesta.raise_for_status()
        datos = respuesta.json()
        return datos["rates"]
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return None
