# Conversor de divisas

## 1. Descripción

Aplicación de consola desarrollada en Python para convertir montos entre USD, EUR y COP. Intenta consultar un servicio externo para obtener las tasas de cambio y utiliza un archivo CSV local como alternativa cuando el servicio no está disponible.

Las tasas incluidas en el CSV son datos de demostración y no deben utilizarse para operaciones financieras reales.

## 2. Requisitos

- Python 3.11 o superior.
- Conexión a Internet para consultar un servicio externo.
- Dependencias indicadas en `requirements.txt`.

## 3. Instalación

Abre una terminal en la carpeta del proyecto y crea un entorno virtual:

    python -m venv .venv

Activa el entorno virtual en Windows con Git Bash:

    source .venv/Scripts/activate

Instala las dependencias:

    python -m pip install -r requirements.txt

## 4. Configuración

Crea el archivo de configuración privado a partir del ejemplo.

En Windows con Git Bash, ejecuta:

    cp config.example.json config.json

Abre `config.json` y configura los valores correspondientes:

- `api_key`: clave proporcionada por el servicio de tasas de cambio.
- `api_url`: dirección del endpoint compatible con el formato esperado por el programa.

El archivo `config.json` está excluido de Git porque puede contener credenciales privadas. No compartas ni publiques ese archivo.

El valor de `api_url` incluido en el ejemplo es ilustrativo y debe reemplazarse por la dirección de un servicio real. Si el servicio no está disponible, el programa intentará utilizar las tasas locales de `datos/tasas.csv`.

## 5. Ejecución

Desde la carpeta del proyecto, con el entorno virtual activado, ejecuta:

    python main.py

Ingresa el monto y las monedas cuando el programa lo solicite.

## 6. Ejemplo de uso

Entrada:

    Ingrese el monto que desea convertir: 100
    Moneda de origen (USD, EUR, COP): USD
    Moneda de destino (USD, EUR, COP): EUR

Salida ilustrativa cuando se utilizan las tasas locales:

    Se utilizarán las tasas locales de respaldo.
    -----------------------------------
    RESUMEN DE LA CONVERSIÓN
    Monto original: 100.00 USD
    Tasa aplicada: 0.92
    Resultado: 92.00 EUR
    -----------------------------------
    Gracias por utilizar el conversor.

El resultado depende de las tasas disponibles en el archivo CSV o del servicio externo configurado.

## 7. Dependencias

Las dependencias y sus versiones se encuentran registradas en `requirements.txt`. Para instalarlas se utiliza:

    python -m pip install -r requirements.txt
