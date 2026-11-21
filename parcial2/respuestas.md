# PARCIAL 2 - INGENIERÍA DE SOFTWARE Y EVALUACIÓN DE AGENTES

**Estudiante:** Víctor Manuel Cañas Salazar  
**Evaluación:** Parcial Técnico 2  
**Valor:** 100 puntos

---

## Pregunta 1. Revisión de código y clasificación de hallazgos

### 1.1. Hallazgos identificados

Se revisó la función `obtener_usuario`, teniendo en cuenta los posibles errores de corrección, comprensibilidad y cumplimiento de normas de desarrollo. Se identificaron cinco hallazgos.

#### Hallazgo 1. Construcción insegura de la consulta SQL

- **Línea:** 2.
- **Severidad:** Crítica.
- **Categoría:** Corrección.
- **Problema:** La consulta SQL se construye concatenando directamente el valor de `user_id`. Esto permite que una entrada manipulada cambie la estructura de la consulta.
- **Escenario de fallo:** Si el identificador recibido contiene caracteres y expresiones SQL inesperadas, la consulta podría ejecutar una condición diferente de la prevista. Esto puede permitir consultar información que no corresponde al usuario solicitado.
- **Corrección propuesta:** Utilizar parámetros en la consulta, en lugar de concatenar el dato recibido.

Código actual:

```python
query = "SELECT * FROM usuarios WHERE id = '" + user_id + "'"
cur = conn.execute(query)
```

Código corregido:

```python
query = "SELECT * FROM usuarios WHERE id = ?" 
cur = conn.execute(query, (user_id,))
```

La consulta parametrizada permite que el valor de user_id sea tratado como un dato y no como parte de las instrucciones SQL.
#### Hallazgo 2. Consulta repetida dentro de un ciclo (problema N+1)
- Líneas: 7 a 10.
- Severidad: Alta, dependiendo del volumen de resultados y de la latencia de la base de datos.
- Categoría: Corrección.
- Problema: Por cada usuario obtenido en la primera consulta se ejecuta otra consulta para recuperar sus permisos. Esto genera una consulta adicional por cada fila.
- Escenario de fallo: Si la consulta inicial devuelve 100 usuarios, se pueden ejecutar 101 consultas en total: una consulta inicial y otras 100 para recuperar los permisos. Con muchos registros, el tiempo de respuesta puede aumentar considerablemente.
- Corrección propuesta: Recuperar los usuarios y sus permisos mediante una consulta con JOIN, o utilizar una consulta por lotes que obtenga los permisos de todos los usuarios encontrados.
La solución debe conservar la relación correcta entre cada usuario y sus permisos, evitando ejecutar una consulta individual en cada iteración.
#### Hallazgo 3. Parámetro rol que no se utiliza
- Línea: 1.
- Severidad: Media.
- Categoría: Corrección.
- Problema: La función recibe el parámetro rol, cuyo valor predeterminado es "lector", pero nunca lo utiliza.
- Escenario de fallo: Si quien llama a la función espera que el rol recibido influya en los datos consultados o en los permisos devueltos, la función no cumplirá esa expectativa. Por ejemplo, pasar un rol diferente no produce ningún cambio en el resultado.
- Corrección propuesta: Si el rol forma parte del comportamiento esperado, implementar y probar la lógica correspondiente. Si no tiene ninguna función, eliminar el parámetro de la firma para evitar confusión.
Aclaración: El código por sí solo no demuestra que exista un requisito de autorización basado en roles. Por eso, el problema confirmado es que el parámetro no se utiliza; afirmar que existe una vulnerabilidad de autorización requeriría conocer los requisitos de la aplicación.
#### Hallazgo 4. Uso de SELECT *
- Líneas: 2 y 9.
- Severidad: Baja.
- Categoría: Comprensibilidad.
- Problema: Las dos consultas utilizan SELECT *, por lo que recuperan todas las columnas disponibles aunque la función no necesariamente las necesita.
- Escenario de fallo: Si la tabla incorpora nuevas columnas, la función puede comenzar a recuperar información adicional sin que exista una necesidad explícita. También puede aumentar el volumen de datos transferidos y hacer menos claro qué información necesita cada operación.
- Corrección propuesta: Especificar las columnas requeridas en cada consulta. Por ejemplo, recuperar únicamente el identificador y los campos necesarios del usuario, y las columnas necesarias de sus permisos.
Esto hace que las consultas sean más claras y reduce la dependencia de la estructura completa de las tablas.
#### Hallazgo 5. Recuperación de todas las filas para devolver solamente la primera
- Líneas: 4, 13 y 14.
- Severidad: Baja.
- Categoría: Cumplimiento de normas.
- Problema: La función recupera todos los usuarios encontrados mediante fetchall(), pero posteriormente solamente devuelve el primer resultado. Esto puede generar trabajo y consumo de memoria innecesarios.
- Escenario de fallo: Si la consulta devuelve varios registros, la función almacena todos en memoria aunque solamente utiliza el primero. Esto puede afectar la eficiencia cuando el conjunto de resultados es grande.
- Corrección propuesta: Si user_id identifica un único usuario, se puede utilizar fetchone() en la consulta de usuarios para recuperar solamente ese registro. El fetchall() de la consulta de permisos debe conservarse si un usuario puede tener varios permisos.
Aclaración sobre la categoría: Esta clasificación como cumplimiento de normas supone que el proyecto establece una convención de utilizar fetchone() cuando solamente se necesita un registro. Si esa convención no existe, el hallazgo se entiende mejor como una observación de eficiencia. La categoría no se puede confirmar sin conocer las normas internas del equipo.
### 1.2. Orden de los hallazgos por severidad y justificación
El orden propuesto, desde el riesgo más alto hasta el más bajo, es el siguiente:

| Orden | Hallazgo | Severidad | Justificación |
|---|---|---|---|
| 1 | Construcción insegura de SQL | Crítica | Puede permitir alterar la consulta y acceder a información no prevista. |
| 2 | Consulta N+1 | Alta | Puede afectar considerablemente el rendimiento cuando aumenta el número de usuarios. |
| 3 | Parámetro rol sin uso | Media | Puede causar un comportamiento diferente al esperado por quien utiliza la función. |
| 4 | Uso de SELECT * | Baja | Reduce la claridad y puede recuperar información innecesaria. |
| 5 | fetchall() cuando solo se devuelve el primero | Baja | Puede desperdiciar memoria y trabajo de procesamiento. |

Los hallazgos 2 y 3 requieren contexto para determinar su impacto exacto:
- Consulta N+1: su severidad depende del volumen de datos, la frecuencia de ejecución y el tiempo de respuesta de la base de datos. En una operación con pocos registros podría tener un impacto limitado; en una operación de alto tráfico podría convertirse en un problema importante.
- Parámetro rol: su severidad depende de los requisitos de la función. Si el rol debía controlar el acceso o modificar el comportamiento, el problema podría tener un impacto mayor. Sin esos requisitos, no es correcto afirmar que existe una vulnerabilidad de autorización.
### 1.3. Política para bloquear o permitir la integración del código
Propongo utilizar una política basada en la severidad y en la evidencia del hallazgo:

| Severidad | Política | Justificación |
|---|---|---|
| Crítica | Bloquear la integración. | Representa un riesgo importante que debe corregirse antes de incorporar el cambio. |
| Alta | Bloquear cuando el impacto esté confirmado o exista evidencia suficiente de un riesgo importante. | Evita incorporar problemas graves de rendimiento o funcionamiento. |
| Media | Solicitar revisión y corrección según los requisitos del proyecto. | Puede representar un problema real, pero necesita contexto para determinar su impacto. |
| Baja | Registrar como observación y permitir la integración, salvo que exista una norma obligatoria incumplida. | Evita bloquear cambios por asuntos menores que no representan un riesgo inmediato. |

El objetivo es evitar dos extremos:
1. Bloqueos por falsos positivos: si una herramienta identifica un problema que realmente no existe o cuya gravedad fue exagerada, puede detener trabajo válido y reducir la confianza del equipo en la revisión automatizada.
2. Hallazgos decorativos que nunca bloquean: si todos los problemas se muestran como simples advertencias, incluso los críticos, el proceso pierde capacidad para prevenir errores importantes.
Para esta función, la construcción insegura de SQL debe bloquear la integración hasta que se corrija y se compruebe la solución. La consulta N+1 debe revisarse con especial atención y bloquearse si las condiciones de uso demuestran un impacto significativo. Los hallazgos de severidad media o baja deben tratarse según los requisitos y las normas verificables del proyecto.


---

## Pregunta 2. Análisis comparativo de herramientas de revisión de código

### 2.1. Capacidad de los analizadores estáticos y de los agentes de IA

Los analizadores estáticos y los agentes de inteligencia artificial pueden detectar problemas de código, pero trabajan de maneras diferentes. Un analizador estático utiliza reglas, patrones y análisis del código para identificar situaciones conocidas. Un agente de IA puede interpretar descripciones, requisitos y contexto, por lo que puede ayudar a reconocer problemas que no se identifican fácilmente mediante reglas tradicionales.

| Defecto | Analizador estático | Agente de IA | Explicación |
|---|---|---|---|
| Variable declarada y no utilizada | Alta | Alta | Es un patrón que puede detectarse mediante reglas y también mediante revisión del código. |
| Clave API escrita directamente en el código | Media o alta con herramientas especializadas | Alta, si recibe el contexto | Las herramientas de detección de secretos pueden identificar patrones de credenciales. El agente también puede reconocer una posible exposición. |
| Condición lógica invertida | Limitada | Potencialmente alta | Para determinar si una condición está invertida normalmente se necesita conocer el comportamiento esperado. |
| Consulta N+1 | Variable | Potencialmente alta | Las herramientas especializadas pueden detectar patrones conocidos; el agente puede analizar el contexto de las consultas y los ciclos. |
| Documentación que indica promedio, mientras el código calcula mediana | Muy limitada | Potencialmente alta | Se necesita comparar el significado de la documentación con la operación implementada. |

Un analizador estático no siempre puede determinar que una condición es incorrecta si no conoce el requisito funcional. Por ejemplo, una comparación puede ser válida desde el punto de vista sintáctico, pero incumplir una regla de negocio. En ese caso, proporcionar al agente la especificación correspondiente puede mejorar el análisis.

Sin embargo, la inteligencia artificial tampoco garantiza una conclusión correcta. Puede interpretar mal los requisitos, generar falsos positivos o no identificar un defecto.

### 2.2. Comparación de ventajas y limitaciones

| Criterio | Analizador estático | Agente de IA |
|---|---|---|
| Repetibilidad | Generalmente alta, porque aplica reglas definidas. | Puede variar entre ejecuciones. |
| Velocidad | Normalmente rápida y adecuada para ejecutarse en cada cambio. | Puede requerir llamadas a un modelo remoto y aumentar el tiempo de revisión. |
| Contexto | Depende de las reglas y del alcance del análisis. | Puede interpretar código, documentación y requisitos proporcionados. |
| Explicación | Presenta reglas, ubicaciones y mensajes definidos. | Puede generar explicaciones y recomendaciones en lenguaje natural. |
| Falsos positivos | Dependen de las reglas y de la configuración. | Puede producir hallazgos que parecen razonables, pero no corresponden a defectos reales. |
| Costos | Puede ejecutarse localmente, aunque algunas soluciones tienen licencias. | Puede generar costos por uso del modelo y consumo de recursos. |
| Privacidad | Puede analizarse localmente. | Si se utiliza un servicio remoto, debe revisarse qué información se envía. |

Considero que ambas herramientas deben complementarse. Los analizadores estáticos son adecuados para identificar problemas conocidos de manera repetible, mientras que un agente puede aportar una revisión contextual que ayude a interpretar requisitos y explicar posibles defectos.

### 2.3. Razones por las que una organización podría no adoptar un agente de IA

Una organización puede decidir no adoptar un agente de revisión de código por diferentes motivos:

1. **Falta de confianza:** si el agente produce falsos positivos o no detecta defectos importantes, el equipo puede perder confianza en sus recomendaciones.
2. **Costos:** las llamadas a modelos remotos pueden aumentar los gastos de operación.
3. **Privacidad y seguridad:** el código fuente puede contener información confidencial que no debe enviarse a servicios externos sin autorización.
4. **Tiempo de revisión:** si el agente demora demasiado, puede afectar el flujo de integración continua.
5. **Mantenimiento:** los modelos, instrucciones y criterios de evaluación necesitan seguimiento y actualización.
6. **Responsabilidad:** una recomendación automática no reemplaza la revisión de una persona responsable del cambio.

Mi recomendación sería comenzar con un piloto controlado. El agente debería funcionar como apoyo para los desarrolladores y no como único responsable de aprobar o rechazar cambios. Antes de permitir que bloquee integraciones, la organización debe comprobar su precisión, exhaustividad, estabilidad y comportamiento ante código limpio.

---

## Pregunta 3. Clasificación de pruebas y estabilidad de la suite

### 3.1. Clasificación de las pruebas por tamaño

Para clasificar las pruebas considero el aislamiento, las dependencias externas, los servicios utilizados y el tiempo de ejecución. Una prueba pequeña debe ser rápida y aislada; una mediana puede utilizar servicios locales; una grande puede depender de sistemas externos o de una integración amplia.

| Prueba | Descripción | Tiempo | Tamaño | Justificación |
|---|---|---:|---|---|
| T1 | Prueba de una función de formato | 12 ms | Small | Comprueba una función aislada, sin depender de servicios externos. |
| T2 | Prueba con base de datos en contenedor | 4.2 s | Medium | Necesita una base de datos, pero puede ejecutarse en un entorno local controlado. |
| T3 | Prueba contra una API pública de terceros | 1.8 s | Large | Depende de la red y de la disponibilidad de un servicio externo. |
| T4 | Prueba completa del agente con modelo remoto y repositorio | 31 s | Large | Integra varios componentes y depende de una llamada remota al modelo. |
| T5 | Prueba de un parser con entradas malformadas | 8 ms | Small | Puede ejecutarse de forma aislada con entradas controladas. |
| T6 | Prueba que inicia un servicio y realiza HTTP local | 2.6 s | Medium | Utiliza un servicio local y comprueba la comunicación entre componentes. |

### 3.2. Distribución de tamaños

La suite tiene seis pruebas:

- Small: 2 pruebas.
- Medium: 2 pruebas.
- Large: 2 pruebas.

El porcentaje se calcula dividiendo la cantidad de pruebas de cada tamaño entre el total:

- Small: (2 / 6) × 100 = 33.33 %.
- Medium: (2 / 6) × 100 = 33.33 %.
- Large: (2 / 6) × 100 = 33.33 %.

| Tamaño | Distribución actual | Distribución recomendada de referencia |
|---|---:|---:|
| Small | 33.33 % | 80 % |
| Medium | 33.33 % | 15 % |
| Large | 33.33 % | 5 % |

La distribución actual no es equilibrada frente a la referencia propuesta. Las pruebas pequeñas representan solamente un tercio de la suite, mientras que las pruebas grandes representan otro tercio. Esto puede generar retroalimentación lenta y una mayor dependencia de servicios externos.

La cantidad de pruebas grandes es aproximadamente 6.67 veces la proporción de referencia. Por tanto, convendría aumentar las pruebas pequeñas y reducir las dependencias externas de las pruebas que se ejecutan frecuentemente.

### 3.3. Pruebas con mayor riesgo de inestabilidad

Identifico dos pruebas especialmente sensibles a factores externos:

**T3: prueba contra una API pública.**

Puede fallar por problemas de conexión, indisponibilidad del proveedor, límites de solicitudes, cambios en los datos o modificaciones del contrato de la API. Una falla no necesariamente significa que el código propio esté defectuoso.

Propondría utilizar mocks o pruebas de contrato para la ejecución habitual de CI. También mantendría una prueba de integración real, ejecutada de forma controlada, con tiempos de espera y manejo de errores.

**T4: prueba completa del agente con un modelo remoto.**

Los modelos de inteligencia artificial pueden generar respuestas diferentes incluso cuando reciben entradas similares. También pueden presentarse cambios en el servicio, latencia, límites de uso y errores de conexión.

Para mejorar su estabilidad, utilizaría respuestas simuladas en las pruebas unitarias y de integración que verifican el procesamiento del agente. Las evaluaciones reales del modelo se ejecutarían por separado, con casos conocidos, criterios de aceptación y varias repeticiones.

No sería suficiente comprobar que el agente produce tres hallazgos. También se debe verificar que esos hallazgos correspondan a los defectos esperados, tengan evidencia y no sean observaciones irrelevantes.

### 3.4. Consecuencias de ignorar las pruebas inestables

Ignorar las pruebas inestables puede generar una cultura en la que el equipo deja de confiar en los resultados de CI. Si una prueba falla ocasionalmente y luego pasa al repetirla, los desarrolladores pueden acostumbrarse a ignorar las alertas.

Esto tiene varias consecuencias:

- Se pueden ocultar defectos reales entre fallas intermitentes.
- Los desarrolladores pueden dejar de investigar los errores.
- Los resultados de CI pierden credibilidad.
- Se pueden introducir cambios defectuosos porque las pruebas no ofrecen una señal confiable.

Propongo registrar cada prueba inestable con una persona responsable, una incidencia y un plazo de corrección. Si es necesario aislarla temporalmente, debe mantenerse identificada y no eliminarse. Los reintentos pueden ayudar a diagnosticar el problema, pero no deben convertirse en la solución definitiva.

---

## Pregunta 4. Análisis y corrección de un workflow de integración continua

### 4.1. Problemas del workflow presentado en el enunciado

El workflow de ejemplo contiene varios problemas de seguridad, estructura y confiabilidad:

1. **Secreto expuesto:** una clave API escrita directamente en el archivo YAML puede quedar almacenada en el repositorio y en su historial. Si una clave real fue publicada, debe revocarse y reemplazarse inmediatamente.
2. **Indentación incorrecta:** las propiedades de los jobs, los pasos y las variables de entorno deben estar ubicadas en los niveles correspondientes. Una estructura incorrecta puede impedir que GitHub Actions interprete el archivo.
3. **Ruta del agente:** el ejemplo utiliza `agente/revisar.py`, pero el proyecto real contiene `agent/agent.py`. No se debe asumir que existe una ruta o una interfaz de línea de comandos que no está implementada.
4. **Nombre de la variable:** el agente real obtiene la credencial mediante `GROQ_API_KEY`. Utilizar `API_KEY` no satisface ese requisito.
5. **Pruebas que no bloquean:** utilizar `pytest tests/ || true` oculta el código de error de pytest. Por tanto, una prueba fallida podría terminar reportándose como una ejecución exitosa.
6. **Versión de Python:** no establecer una versión explícita puede reducir la reproducibilidad del entorno.
7. **Mensaje de éxito engañoso:** imprimir "Revisión completada" no demuestra que la revisión o las pruebas hayan sido correctas.

Si la clave API del ejemplo fuera real, editar el archivo no sería suficiente. También se debería revocar la credencial, revisar su uso y evaluar la exposición en el historial del repositorio.

### 4.2. Workflow corregido para las pruebas del proyecto

El proyecto real utiliza Python 3.11, contiene un directorio `tests/` y tiene un archivo `requirements.txt`. Por eso, propongo el siguiente workflow para ejecutar pruebas automatizadas sin realizar llamadas innecesarias al modelo remoto:

```yaml
name: CI - pruebas del agente

on:
  pull_request:
    branches: [main, master]
  push:
    branches: [main, master]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  pruebas:
    name: Pruebas automatizadas
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Descargar el repositorio
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Instalar dependencias
        run: python -m pip install -r requirements.txt

      - name: Ejecutar pruebas
        run: python -m pytest tests/ -q
```

Esta propuesta utiliza permisos mínimos de lectura, configura una versión definida de Python y ejecuta pytest sin ocultar sus errores.

La ejecución de pruebas no necesita una clave API si las pruebas están diseñadas para utilizar dependencias simuladas o no requieren conectarse al modelo. Si se necesita evaluar el modelo real, esa evaluación debe separarse y utilizar una credencial almacenada en GitHub Actions Secrets, bajo el nombre `GROQ_API_KEY`.

### 4.3. Diferencia entre el ejemplo defectuoso y el workflow real

Al revisar el proyecto encontré el archivo `.github/workflows/ci.yml`.

El workflow real ya tiene varios aspectos correctamente implementados:

- Se ejecuta en `push`, `pull_request` y `workflow_dispatch`.
- Configura Python 3.11.
- Instala las dependencias.
- Ejecuta `python -m pytest -q`.
- Utiliza permisos `contents: read`.
- No contiene una clave API escrita directamente en el archivo.
- No utiliza `|| true` para ocultar fallos.

Por lo tanto, no sería correcto afirmar que el workflow real tiene todos los errores del ejemplo del enunciado. La propuesta anterior es una versión mejorada y específica para las pruebas del proyecto.

---

## Pregunta 5. Evaluación de resultados, métricas y confiabilidad

### 5.1. Cálculo de las métricas del escenario del enunciado

Para comparar las tres corridas utilizo las siguientes fórmulas:

**Precisión:**

Precisión = TP / (TP + FP)

Mide qué proporción de las detecciones positivas corresponde a verdaderos positivos.

**Exhaustividad (Recall):**

Exhaustividad = TP / (TP + FN)

Mide qué proporción de los defectos existentes fue detectada.

**F1:**

F1 = 2 × (Precisión × Exhaustividad) / (Precisión + Exhaustividad)

También puede calcularse directamente como:

F1 = 2TP / (2TP + FP + FN)

Los datos del escenario son:

| Corrida | TP | FP | FN |
|---|---:|---:|---:|
| 1 | 7 | 3 | 4 |
| 2 | 9 | 5 | 2 |
| 3 | 6 | 2 | 5 |

**Corrida 1**

Precisión = 7 / (7 + 3) = 7 / 10 = 0.7000 = 70.00 %.

Exhaustividad = 7 / (7 + 4) = 7 / 11 = 0.6364 = 63.64 %.

F1 = (2 × 7) / (14 + 3 + 4) = 14 / 21 = 0.6667 = 66.67 %.

**Corrida 2**

Precisión = 9 / (9 + 5) = 9 / 14 = 0.6429 = 64.29 %.

Exhaustividad = 9 / (9 + 2) = 9 / 11 = 0.8182 = 81.82 %.

F1 = (2 × 9) / (18 + 5 + 2) = 18 / 25 = 0.7200 = 72.00 %.

**Corrida 3**

Precisión = 6 / (6 + 2) = 6 / 8 = 0.7500 = 75.00 %.

Exhaustividad = 6 / (6 + 5) = 6 / 11 = 0.5455 = 54.55 %.

F1 = (2 × 6) / (12 + 2 + 5) = 12 / 19 = 0.6316 = 63.16 %.

### 5.2. Comparación de las tres corridas

| Métrica | Corrida 1 | Corrida 2 | Corrida 3 | Promedio |
|---|---:|---:|---:|---:|
| Precisión | 70.00 % | 64.29 % | 75.00 % | 69.76 % |
| Exhaustividad | 63.64 % | 81.82 % | 54.55 % | 66.67 % |
| F1 | 66.67 % | 72.00 % | 63.16 % | 67.27 % |

El promedio de precisión se calcula así:

(70.00 + 64.29 + 75.00) / 3 = 69.76 %.

El promedio de exhaustividad es:

(63.64 + 81.82 + 54.55) / 3 = 66.67 %.

El promedio de F1, calculado con los valores sin redondear, es:

[(14/21) + (18/25) + (12/19)] / 3 = 67.27 % aproximadamente.

La métrica que presenta mayor variación es la exhaustividad:

81.82 % - 54.55 % = 27.27 puntos porcentuales.

Esto indica que la cantidad de defectos detectados cambia considerablemente entre corridas. La segunda corrida obtiene la mayor exhaustividad, pero también tiene la menor precisión. La tercera obtiene la mayor precisión, pero deja sin detectar una mayor cantidad de defectos.

Por tanto, no conviene seleccionar solamente la segunda corrida para presentar el desempeño del sistema. Es necesario informar las tres y considerar sus diferencias.

### 5.3. Inconsistencia en los falsos positivos del escenario

El enunciado indica que existen cuatro casos limpios, pero la segunda corrida presenta cinco falsos positivos.

Si cada caso limpio puede contarse como máximo una vez como falso positivo, el número de falsos positivos no puede superar cuatro. Por tanto, los datos de esa corrida presentan una inconsistencia que debe aclararse.

Si los falsos positivos representan hallazgos individuales y no casos limpios marcados incorrectamente, entonces no se pueden interpretar directamente como cantidad de casos limpios afectados.

La tasa de falsos positivos a nivel de caso se calcula así:

FPR = FP / (FP + TN).

Como existen cuatro controles limpios, FP + TN debería ser igual a cuatro si cada control se clasifica una sola vez.

No es correcto presentar una tasa de falsos positivos válida para la segunda corrida sin aclarar cómo se contabilizaron esos cinco falsos positivos.

### 5.4. Comparación con los resultados reales del proyecto

Además de los datos del escenario anterior, revisé los archivos reales de evaluación del proyecto:

- `eval/resultados/eval_run_1.json`
- `eval/resultados/eval_run_2.json`
- `eval/resultados/eval_run_3.json`

Las tres ejecuciones registran los siguientes resultados:

| Métrica | Corrida 1 | Corrida 2 | Corrida 3 |
|---|---:|---:|---:|
| Casos evaluados | 15 | 15 | 15 |
| Verdaderos positivos | 11 | 11 | 11 |
| Falsos positivos | 0 | 0 | 0 |
| Falsos negativos | 0 | 0 | 0 |
| Precisión | 100 % | 100 % | 100 % |
| Exhaustividad | 100 % | 100 % | 100 % |
| F1 | 100 % | 100 % | 100 % |
| Tiempo | 27.845 s | 41.957 s | 34.180 s |

Los tres resultados muestran que el agente detectó los once casos con defectos y no marcó como defectuosos los cuatro controles limpios.

El tiempo promedio de ejecución fue:

(27.845 + 41.957 + 34.180) / 3 = 34.661 segundos aproximadamente.

Estos resultados son positivos, pero deben interpretarse considerando la metodología del evaluador. El propio archivo de resultados aclara que la detección se mide a nivel de caso: un caso se considera detectado cuando aparece al menos un hallazgo.

Por consiguiente, estas métricas no demuestran que cada hallazgo sea semánticamente correcto, que tenga la ubicación exacta o que todos los problemas adicionales reportados sean defectos reales.

### 5.5. Comparación con Ruff y Bandit

También se ejecutó una evaluación de analizadores estáticos, cuyos resultados se encuentran en `eval/resultados/static_analyzer_eval.json`.

| Herramienta | TP | FP | FN | TN | Precisión | Exhaustividad | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Ruff | 2 | 0 | 9 | 4 | 100 % | 18.18 % | 30.77 % |
| Bandit | 2 | 0 | 9 | 4 | 100 % | 18.18 % | 30.77 % |

En esta evaluación, Ruff identificó dos casos mediante advertencias relacionadas con la organización de imports. Esto demuestra una limitación del criterio de evaluación: detectar una advertencia en un caso no significa necesariamente identificar el defecto que se quería probar.

Bandit identificó dos casos de seguridad, relacionados con una posible inyección SQL y la ejecución de procesos mediante shell.

La comparación muestra que los analizadores estáticos pueden identificar patrones concretos con utilidad, mientras que el agente obtuvo mayor cobertura en el conjunto evaluado. Sin embargo, no se puede concluir que el agente sea superior en todos los escenarios, porque el resultado depende de los casos seleccionados y del criterio utilizado para contar una detección.

### 5.6. Recomendación sobre el uso del agente en producción

No recomendaría utilizar el agente como único mecanismo para aprobar automáticamente cambios de código en producción.

Antes de adoptar esa decisión, implementaría las siguientes mejoras:

1. Validar cada hallazgo contra el defecto esperado, incluyendo categoría, evidencia y ubicación.
2. Ampliar el conjunto de pruebas con casos nuevos y representativos.
3. Repetir las evaluaciones para medir la estabilidad del agente.
4. Comprobar que los controles limpios no reciban hallazgos incorrectos.
5. Separar las pruebas deterministas de las evaluaciones que dependen del modelo remoto.
6. Establecer umbrales mínimos de precisión y exhaustividad antes de permitir que el agente bloquee integraciones.
7. Mantener una revisión humana para los hallazgos críticos y aquellos que dependan del contexto del negocio.
8. Revisar los costos, la privacidad del código y la disponibilidad del servicio remoto.

Mi conclusión es que el agente presenta resultados prometedores en las pruebas realizadas, pero todavía necesita una evaluación más rigurosa de la calidad individual de sus hallazgos. Lo utilizaría inicialmente como herramienta de apoyo para los desarrolladores, combinándolo con analizadores estáticos y pruebas automatizadas tradicionales.

---

## Conclusión general del parcial

El análisis realizado permite comprender que la calidad de una herramienta de revisión de código no depende únicamente de cuántos problemas detecta. También es necesario evaluar si los hallazgos son correctos, si se pueden reproducir, cuánto tiempo requiere el análisis y qué riesgos introduce en el proceso de desarrollo.

Los analizadores estáticos ofrecen resultados útiles y repetibles para patrones conocidos. Los agentes de inteligencia artificial pueden complementar ese trabajo mediante la interpretación de contexto y la generación de explicaciones, pero necesitan controles para evitar errores y conclusiones sin evidencia.

Por esa razón, considero que la estrategia más adecuada es combinar pruebas automatizadas, analizadores estáticos, evaluación controlada del agente y revisión humana. Esta combinación permite aprovechar las ventajas de cada herramienta sin depender completamente de una sola.