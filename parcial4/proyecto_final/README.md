# Conversor de divisas

## 1. Descripción

Este proyecto es una reconstrucción demostrativa de un conversor de divisas en Python. Permite convertir montos entre USD, EUR y COP utilizando tasas obtenidas desde un servicio externo compatible o, si el servicio no está disponible, tasas locales almacenadas en un archivo CSV.

**Nota sobre el alcance:** el enunciado describe un proyecto original entregado en un archivo ZIP, pero no se proporcionó ese ZIP ni su código fuente. Por esta razón, el proyecto inicial y el proyecto refactorizado se reconstruyeron a partir de la descripción del caso. No se afirma que el código reconstruido sea el original ni que se haya refactorizado el archivo original de 180 líneas.

## 2. Requisitos

- Python 3.11 o una versión posterior.
- pip.
- Conexión a Internet únicamente para intentar consultar un servicio externo compatible.

Las dependencias de Python están especificadas con versiones fijas en `requirements.txt`.

## 3. Estructura del proyecto

- `main.py`: coordina la ejecución, solicita los datos al usuario y presenta el resultado.
- `converter.py`: contiene la lógica de conversión, la lectura de tasas desde CSV y la consulta del servicio externo.
- `utils.py`: contiene funciones para validar, interpretar y formatear montos.
- `config.example.json`: plantilla de configuración.
- `config.json`: configuración local. No debe incluirse en Git.
- `datos/tasas.csv`: tasas locales de demostración.
- `tests/test_converter.py`: pruebas automatizadas.
- `requirements.txt`: dependencias con versiones fijadas.

## 4. Instalación

Desde la carpeta del proyecto, crear un entorno virtual:

    python -m venv .venv

En Git Bash para Windows, activarlo con:

    source .venv/Scripts/activate

En Windows PowerShell, activarlo con:

    .venv\Scripts\Activate.ps1

Instalar las dependencias:

    python -m pip install -r requirements.txt

## 5. Configuración

Crear el archivo de configuración local a partir de la plantilla:

    cp config.example.json config.json

En Windows PowerShell también se puede utilizar:

    Copy-Item config.example.json config.json

Editar `config.json` y establecer la dirección y la clave correspondientes a un servicio de tasas de cambio que sea compatible con la estructura esperada por el programa.

La dirección incluida en la configuración de ejemplo es ilustrativa. No representa un servicio real verificado y la clave de ejemplo no es una credencial válida.

**Importante:** `config.json` contiene configuración privada y está excluido del control de versiones mediante `.gitignore`. No se deben publicar claves reales.

## 6. Ejecución

Con el entorno virtual activo y la configuración creada:

    python main.py

El programa solicita el monto, la moneda de origen y la moneda de destino. Si la consulta externa no está disponible, intenta utilizar las tasas locales de `datos/tasas.csv`.

## 7. Ejemplo de ejecución

Con las tasas locales de demostración, una conversión de 100 USD a EUR utiliza una tasa de 0.92:

    Monto original: 100.00 USD
    Tasa aplicada: 0.92
    Resultado: 92.00 EUR

Las tasas del CSV son datos de demostración y no deben interpretarse como cotizaciones financieras actuales.

## 8. Pruebas automatizadas

Para ejecutar las pruebas:

    python -m unittest discover -s tests -v

La suite comprueba la interpretación de montos, el rechazo de entradas inválidas, las conversiones, la lectura del CSV, el manejo de tasas ausentes, el formato de salida y el comportamiento de la consulta externa mediante respuestas simuladas.

La consulta externa se prueba con mocks para no depender de una API real durante las pruebas automatizadas.

## 9. Separación de responsabilidades

La refactorización demostrativa divide las tareas en tres módulos:

- `utils.py`: validación, interpretación y formato de montos.
- `converter.py`: operaciones de conversión y obtención de tasas.
- `main.py`: interacción con el usuario y coordinación del programa.

Esta separación facilita el mantenimiento y permite probar la lógica sin depender de la entrada y salida de la consola.

## 10. Limitaciones conocidas

- No se recibió el ZIP original descrito en el caso; por tanto, no fue posible inspeccionar ni verificar su código.
- El servicio externo de ejemplo no fue validado contra un proveedor real ni se probaron credenciales reales.
- La ejecución demostrada utiliza las tasas locales de respaldo.
- Los valores del CSV son únicamente datos de demostración.
