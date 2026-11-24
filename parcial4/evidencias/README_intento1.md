# Conversor de divisas

## 1. Descripción

Aplicación de consola desarrollada en Python para convertir montos entre USD, EUR y COP. Consulta un servicio externo para obtener tasas de cambio y utiliza un archivo CSV local como alternativa cuando el servicio no está disponible.

## 2. Requisitos

- Python 3.11 o superior.
- Conexión a Internet para intentar consultar el servicio externo.
- Dependencias indicadas en `requirements.txt`.

## 3. Instalación

Crear y activar un entorno virtual:

```bash
python -m venv .venv


En Windows con Git Bash:
source .venv/Scripts/activate


Instalar las dependencias:
python -m pip install -r requirements.txt


4. Configuración
El programa necesita un archivo config.json con la dirección del servicio y la clave de API.

La estructura de ejemplo se encuentra en config.example.json. Se debe configurar una clave válida para utilizar un servicio compatible.
5. Ejecución
Desde la carpeta del proyecto, ejecutar:
python main.py


6. Ejemplo de uso
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


Las tasas del archivo CSV son datos de demostración y no deben utilizarse para operaciones financieras reales.
