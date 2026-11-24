# Informe de entrega – Parcial 4
**Para:** Compañero encargado del proyecto  
**Asunto:** Organización, refactorización y pruebas del conversor de divisas

## Estado recibido

El caso describe un conversor de divisas entregado sin control de versiones, documentación, dependencias declaradas ni pruebas automatizadas.  
También describe un archivo principal monolítico y un archivo de configuración que contiene una clave de API en texto plano.  
Sin embargo, no se proporcionó el archivo ZIP original ni su código fuente, por lo que se construyó una versión demostrativa a partir de la descripción del enunciado y no se pudo verificar el código original de 180 líneas.

## Cambios realizados

**Control de versiones y seguridad:** se inicializó el seguimiento del trabajo mediante Git y se organizaron los cambios en commits descriptivos. Se agregó `.gitignore` para excluir configuraciones privadas, entornos virtuales y archivos temporales. Se dejó `config.example.json` como plantilla y se excluyó `config.json` del repositorio.

**Empaquetado y documentación:** se incorporó `requirements.txt` con versiones fijadas y un README con requisitos, instalación, configuración, ejecución y pruebas. Se probó el procedimiento documentado en una carpeta limpia. El primer intento falló porque no se había indicado crear `config.json` a partir de la plantilla; se corrigió el README y el segundo intento permitió ejecutar el programa con las tasas locales de respaldo.

**Estructura y refactorización:** la reconstrucción final separa la interacción con el usuario en `main.py`, la lógica de conversión y consulta de tasas en `converter.py`, y la validación y formato de montos en `utils.py`.

**Pruebas:** se implementaron diez pruebas automatizadas que cubren entradas inválidas, montos negativos, conversiones, tasas ausentes, lectura del CSV y consulta simulada de la API. Las diez pruebas finalizaron correctamente. También se ejecutó el conversor completo con el ejemplo de 100 USD a 92 EUR usando la tasa local de demostración.

## Trabajo no realizado y motivos

No se pudo refactorizar ni comparar el código original de 180 líneas porque el ZIP no fue entregado. Tampoco se validó una integración real con un proveedor externo, porque la dirección de API del ejemplo es ilustrativa y no se suministraron un servicio compatible ni credenciales reales. Las tasas del CSV son datos de demostración, no cotizaciones financieras actuales.

## Recomendación

Antes de utilizar o publicar el conversor, se recomienda solicitar el ZIP original, revisar sus funciones y reglas de negocio, configurar un proveedor de tasas real y validar sus respuestas. También se recomienda mantener las credenciales fuera del repositorio, conservar las dependencias fijadas y ejecutar las pruebas automatizadas antes de cada entrega.
