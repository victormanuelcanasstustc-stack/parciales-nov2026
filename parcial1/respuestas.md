# PARCIAL 1 - HERRAMIENTAS DEL INGENIERO

## Pregunta 1. Automatización y procesamiento de archivos con la terminal

### 1.1. Encontrar los diez archivos más grandes

**Objetivo:** identificar los diez archivos de mayor tamaño dentro de la carpeta `parcial1/archivos_prueba`, ordenándolos de mayor a menor.

**Comando utilizado:**

```bash
find parcial1/archivos_prueba -type f -printf '%s\t%p\0' |
sort -z -t $'\t' -k1,1nr |
head -z -n 10 |
while IFS= read -r -d '' registro; do
    size="${registro%%$'\t'*}"
    archivo="${registro#*$'\t'}"
    printf "%8s bytes  %s\n" "$size" "$archivo"
done
```

**Explicación:**

- `find` busca los archivos dentro de la carpeta indicada.
- `-type f` selecciona solamente archivos normales.
- `-printf '%s\t%p\0'` muestra el tamaño en bytes y la ruta del archivo.
- `sort -z` ordena los registros separados por caracteres nulos.
- `-k1,1nr` ordena numéricamente de mayor a menor según el tamaño.
- `head -z -n 10` selecciona los diez primeros resultados.
- El ciclo `while` separa el tamaño y el nombre para mostrarlos de forma legible.

**Resultado obtenido:**

```text
1800 bytes  parcial1/archivos_prueba/presentacion.pptx
1500 bytes  parcial1/archivos_prueba/respaldo.zip
1100 bytes  parcial1/archivos_prueba/registro.dat
 900 bytes  parcial1/archivos_prueba/imagen prueba.bin
 700 bytes  parcial1/archivos_prueba/documento largo.txt
 600 bytes  parcial1/archivos_prueba/copia.bin
 487 bytes  parcial1/archivos_prueba/registro.log
 450 bytes  parcial1/archivos_prueba/datos.csv
 300 bytes  parcial1/archivos_prueba/programa.py
 250 bytes  parcial1/archivos_prueba/tabla.csv
```

**Análisis:** el archivo de mayor tamaño es `presentacion.pptx`, con 1800 bytes. El comando permite identificar rápidamente los archivos que ocupan más espacio dentro de una carpeta.

### 1.2. Contar archivos por extensión

**Objetivo:** recorrer la carpeta y contar cuántos archivos existen de cada extensión.

**Código utilizado:** `parcial1/scripts/pregunta1_2_extensiones.py`

```python
from pathlib import Path
from collections import Counter
import sys

carpeta = Path(
    sys.argv[1] if len(sys.argv) > 1
    else "parcial1/archivos_prueba"
)

if not carpeta.exists() or not carpeta.is_dir():
    raise SystemExit(f"Error: la carpeta no existe: {carpeta}")

conteo = Counter()

for archivo in carpeta.rglob("*"):
    if archivo.is_file():
        extension = archivo.suffix.lower() or "(sin extension)"
        conteo[extension] += 1

print(f"Conteo de archivos por extension en: {carpeta}")
print("-" * 45)

for extension, cantidad in sorted(conteo.items()):
    print(f"{extension:20} {cantidad:>5}")

print("-" * 45)
print(f"Total de archivos: {sum(conteo.values())}")
```

**Explicación:**

- `Path` permite trabajar con rutas y archivos.
- `Counter` permite contar las apariciones de cada extensión.
- `rglob("*")` recorre la carpeta y sus subcarpetas.
- `is_file()` evita contar directorios.
- `suffix` obtiene la extensión del archivo.
- `lower()` convierte las extensiones a minúsculas para agruparlas.
- Los archivos sin extensión se clasifican como `(sin extension)`.

**Resultado obtenido:**

```text
(sin extension)          1
.bin                     2
.csv                     2
.dat                     1
.log                     1
.md                      1
.pptx                    1
.py                      3
.txt                     3
.zip                     1
---------------------------------------------
Total de archivos:      16
```

**Análisis:** se encontraron 16 archivos. Las extensiones `.py` y `.txt` tienen tres archivos cada una; `.bin` y `.csv` tienen dos. Las demás extensiones tienen un archivo cada una.

### 1.3. Buscar tareas pendientes (TODO) en archivos Python modificados durante los últimos siete días

**Objetivo:** localizar comentarios que contengan la palabra `TODO` en archivos Python modificados durante los últimos siete días.

**Script utilizado:** `parcial1/scripts/pregunta1_3_buscar_todo.sh`

```bash
#!/usr/bin/env bash

# Buscar TODO en archivos Python modificados durante los ultimos 7 dias.

find parcial1/archivos_prueba \
  -type f \
  -name "*.py" \
  -mmin -10080 \
  -print0 |
xargs -0 -r grep -nH -- "TODO"
```

**Explicación:**

- `find` busca dentro de la carpeta de prueba.
- `-type f` selecciona únicamente archivos.
- `-name "*.py"` limita la búsqueda a archivos Python.
- `-mmin -10080` selecciona archivos modificados hace menos de 10080 minutos, equivalentes a siete días.
- `-print0` separa las rutas mediante caracteres nulos.
- `xargs -0` recibe correctamente las rutas, incluso si contienen espacios.
- `grep -nH` busca el texto `TODO`, mostrando el nombre del archivo y el número de línea.

**Resultado obtenido:**

```text
parcial1/archivos_prueba/tarea_pendiente.py:1:# TODO: completar la validacion de entrada
```

**Análisis:** se encontró una tarea pendiente en `tarea_pendiente.py`, ubicada en la línea 1. Esto permite localizar rápidamente comentarios que indican trabajo pendiente dentro de un proyecto.

### 1.4. Identificar los cinco mensajes de error más frecuentes

**Objetivo:** analizar el archivo `registro.log`, contar los mensajes que tienen el nivel `ERROR` y mostrar los cinco más frecuentes.

**Script utilizado:** `parcial1/scripts/pregunta1_4_errores.sh`

```bash
#!/usr/bin/env bash

# Contar los mensajes ERROR y mostrar los cinco mas frecuentes.
# Formato esperado: FECHA NIVEL MENSAJE

awk '$2 == "ERROR" {
    mensaje = $3
    for (i = 4; i <= NF; i++) {
        mensaje = mensaje " " $i
    }
    conteo[mensaje]++
}
END {
    for (mensaje in conteo) {
        print conteo[mensaje] "\t" mensaje
    }
}' parcial1/archivos_prueba/registro.log |
sort -t $'\t' -k1,1nr |
head -n 5
```

**Explicación:**

- `awk` procesa el archivo línea por línea.
- `$2 == "ERROR"` selecciona únicamente las líneas cuyo segundo campo corresponde al nivel de error.
- La variable `mensaje` reúne el texto desde el tercer campo hasta el final.
- `conteo[mensaje]++` incrementa el contador de cada mensaje.
- El bloque `END` imprime los mensajes y sus cantidades.
- `sort` organiza los resultados de mayor a menor frecuencia.
- `head -n 5` muestra como máximo cinco resultados.

**Resultado obtenido:**

```text
4   No se pudo conectar a la base de datos
3   Archivo no encontrado
1   Tiempo de espera agotado
```

**Análisis:** el mensaje más frecuente fue `No se pudo conectar a la base de datos`, con cuatro apariciones. En segundo lugar está `Archivo no encontrado`, con tres apariciones. Finalmente, `Tiempo de espera agotado` aparece una vez.

Aunque se solicitaron los cinco mensajes más frecuentes, solamente existen tres mensajes de error diferentes en el archivo de prueba. Por eso el comando devuelve tres resultados y no cinco.

1.5. Manejo de nombres con espacios y saltos de línea

Si se utilizan espacios como separadores, un nombre de archivo que contenga espacios puede interpretarse incorrectamente como varios campos. Si se utilizan saltos de línea como separadores, un nombre que contenga un salto de línea puede dividirse en registros diferentes.

La solución consiste en utilizar el carácter NUL (\0) como delimitador, porque no puede formar parte de un nombre de archivo. Para ello se utilizan find -printf, sort -z, head -z y read -d ''.

Comando corregido de una sola línea:
find parcial1/archivos_prueba -type f -printf '%s\t%p\0' | sort -z -t $'\t' -k1,1nr | head -z -n 10 | while IFS= read -r -d '' registro; do tamano="${registro%%$'\t'*}"; archivo="${registro#*$'\t'}"; printf "%8s  %q\n" "$(numfmt --to=iec --suffix=B "$tamano")" "$archivo"; done

### Conclusión de la pregunta 1

Mediante estos ejercicios se utilizaron herramientas de terminal y Python para automatizar tareas de administración y análisis de archivos. Se identificaron los archivos más grandes, se contaron las extensiones, se localizaron tareas pendientes y se analizaron los mensajes de error de un registro.

Estos procedimientos permiten ahorrar tiempo, organizar mejor la información y detectar problemas de manera más eficiente en un entorno de desarrollo.


correctamente el commit 9. Después se ejecutó git bisect reset para regresar a la rama main.

## Pregunta 2. Git: modelo de datos y recuperación

### 2.1. Grafo de commits resultante

La secuencia produce seis commits:

- A: commit inicial vacío.
- B: commit hijo de A.
- C: commit creado en la rama `rama`, hijo de B.
- D: commit hijo de C.
- E: commit creado en `main`, también hijo de B.
- M: commit de fusión con dos padres: E y D.

**Grafo después de la fusión y antes del reset:**

```text
      C---D
     /     \
A---B       M
     \     /
      E---
```

Después de ejecutar `git branch -D rama` y `git reset --hard HEAD~1`:

- `main` apunta a E.
- `HEAD` apunta a `main` (es una referencia simbólica), por lo que su commit actual también es E.
- C, D y M dejan de ser alcanzables desde las ramas existentes.
- A, B y E siguen siendo alcanzables desde `main`.

**Grafo después del reset:**

```text
   A---B---C---D
     \       \
      E-------M
      ^
   main, HEAD
```

Los commits C, D y M no se eliminan inmediatamente: sus objetos pueden seguir almacenados en Git y M puede localizarse mediante el reflog.

### 2.2. Definición de rama

Una rama en Git es una referencia móvil que apunta a un commit.

### 2.3. Recuperación de C y D

Primero se consulta el registro de movimientos de HEAD:

```bash
git reflog
```

Se identifica la entrada que corresponde al commit M y se copia su hash completo. Después se crea una rama de recuperación:

```bash
 git branch rescate HASH_COMPLETO_DE_M
```

`HASH_COMPLETO_DE_M` debe reemplazarse por el hash real identificado en el reflog.

C y D siguen existiendo porque `git reset --hard` mueve la referencia de la rama y actualiza el estado de trabajo, pero no elimina inmediatamente los objetos de commits. El reflog conserva temporalmente los movimientos anteriores de HEAD. Al recuperar M, también vuelven a ser alcanzables sus padres D y C.

### 2.4. Restaurar el estado anterior al reset

El comando es:

```bash
git reset --hard ORIG_HEAD
```

En esta secuencia, `ORIG_HEAD` conserva la posición anterior al reset, que corresponde a M. El comando mueve nuevamente `main` a M y actualiza el área de preparación y el directorio de trabajo.

### 2.5. Encontrar automáticamente el commit que introdujo el error

Se supone que se conoce un commit bueno y que el commit actual es malo. La secuencia es:

```bash
git bisect start
git bisect bad HEAD
git bisect good HASH_DEL_COMMIT_BUENO
git bisect run COMANDO_DE_LA_SUITE
git bisect reset
```

Se reemplazan los marcadores por el hash del último commit conocido como bueno y por el comando real que ejecuta las pruebas, por ejemplo, `python -m pytest`.

La suite debe devolver código de salida 0 cuando las pruebas pasan y un código distinto de 0 cuando fallan. `git bisect run` ejecuta automáticamente la suite en los commits seleccionados y utiliza esos códigos para clasificar cada versión.

**Cálculo del peor caso:**

Con 15 commits y los extremos ya clasificados (uno bueno y otro malo), existen como máximo 14 posiciones posibles para el primer commit defectuoso. La búsqueda binaria reduce aproximadamente a la mitad las posibilidades en cada ejecución.

\[
\lceil \log_2(14) \rceil
=
\lceil 3.8074 \rceil
=
4
\]

Por tanto, se requieren como máximo 4 ejecuciones adicionales de la suite para localizar el primer commit defectuoso, bajo el supuesto de que el comportamiento de las pruebas permite distinguir correctamente los commits buenos de los malos.

**Comprobación práctica:**

Se creó un repositorio independiente con 15 commits. El primer commit contenía una prueba correcta y el commit 9 introdujo el cambio defectuoso. Se indicó el primer commit como bueno y el último como malo, y se ejecutó:

```bash
git bisect start
git bisect bad HEAD
git bisect good fe4e066
git bisect run ./prueba.sh
```

El resultado real fue:

```text
bc9886e1a314992fdaa6701ec88c67a71341a0f5 is the first bad commit
Commit 9
bisect found first bad commit
```

Git probó automáticamente los commits 8, 11, 10 y 9: cuatro ejecuciones de la prueba. Identificó correctamente el commit 9 como el primero defectuoso. Finalmente, se ejecutó `git bisect reset` y se regresó a `main`, con el repositorio limpio.


cat >> parcial1/respuestas.md <<'EOF'

## Pregunta 3. Depuración sistemática

El problema se clasifica como un fallo intermitente o no determinista: con los mismos datos de entrada, el programa produce ocasionalmente un resultado incorrecto sin generar una excepción. No asumiría que el CSV está dañado; investigaría también el orden de ejecución, el estado compartido, la concurrencia y las condiciones de escritura.

### 3.1. Bitácora de hipótesis

| Paso | Hipótesis | Experimento concreto | Acción según el resultado |
|---|---|---|---|
| 1 | Existe una condición de carrera: varios hilos o procesos modifican simultáneamente una estructura compartida. | Ejecutar 100 veces el mismo archivo primero con un solo trabajador y después con la configuración concurrente. Comparar los resultados mediante SHA-256 y también por contenido: número de filas, columnas, identificadores y valores agregados. | Si el modo secuencial es estable y el concurrente falla, revisar las variables compartidas, los bloqueos y la sincronización. Si ambos fallan, continuar con las demás hipótesis. |
| 2 | El resultado depende del orden de procesamiento de las filas o de un ordenamiento no determinista. | Ejecutar el procesamiento con el mismo CSV en su orden original y en diferentes permutaciones controladas. Revisar las operaciones de agrupación, ordenamiento y selección de registros. | Si cambia el resultado, establecer un orden explícito y estable, incluyendo una segunda clave de desempate, como el identificador del registro. |
| 3 | La lectura por bloques divide registros o maneja incorrectamente valores entrecomillados, delimitadores o saltos de línea. | Procesar el mismo archivo completo y después con diferentes tamaños de bloque. Comparar el número de filas, las columnas, los valores nulos y los registros de cada resultado. | Si las diferencias aparecen al procesar por bloques, corregir los límites de lectura y la configuración del analizador CSV. |
| 4 | Existen registros duplicados, identificadores repetidos o valores nulos que producen resultados incorrectos durante la agregación. | Calcular el total de filas, contar identificadores duplicados, detectar valores nulos y comparar los resultados de cada grupo con una agregación independiente. | Si se encuentran inconsistencias, definir reglas explícitas para duplicados y valores nulos, y validar las cantidades antes y después de cada transformación. |
| 5 | Varios procesos escriben simultáneamente en el mismo archivo de salida o una escritura reemplaza el resultado de otra. | Ejecutar la transformación sin concurrencia y guardar cada resultado en un archivo temporal diferente. Comparar los archivos y revisar si existe más de un escritor para el mismo destino. | Si el problema desaparece, asignar un único responsable de escritura o utilizar archivos temporales independientes y una sustitución atómica al finalizar. |
| 6 | El comportamiento depende de una configuración o de un estado externo que no se está registrando. | Repetir la ejecución conservando las versiones de Python y las dependencias, la configuración, la semilla aleatoria, la codificación y las variables de entorno. Comparar los metadatos entre ejecuciones. | Si se identifica una diferencia, fijar la configuración necesaria y registrar sus valores para poder reproducir el entorno. |

En todos los experimentos conservaría una copia del archivo original, calcularía su hash SHA-256 y registraría el identificador de cada ejecución. Así se evita confundir un cambio de entrada con un fallo del procesamiento.

### 3.2. Por qué la depuración mediante impresiones es inadecuada

Hay dos razones técnicas principales:

1. **Puede modificar el comportamiento temporal del programa.** Agregar impresiones introduce operaciones de entrada y salida que consumen tiempo y pueden cambiar la planificación de los hilos. Si existe una condición de carrera, el cambio de tiempos puede hacer que el error desaparezca o que aparezca con otra frecuencia. Esto dificulta investigar un fallo que ocurre aproximadamente una de cada veinte ejecuciones.

2. **No proporciona trazabilidad estructurada de las ejecuciones.** Las impresiones aisladas no garantizan que se pueda relacionar cada registro con un archivo, una ejecución, un trabajador o una etapa concreta. En un procesamiento concurrente, los mensajes pueden intercalarse y dificultar la reconstrucción del orden real de los acontecimientos.

Por estas razones utilizaría registros estructurados, con marcas de tiempo, identificadores de ejecución y datos de contexto, en lugar de depender de impresiones dispersas.

### 3.3. Configuración de registro estructurado

Dejaría instalado un registro en formato JSON, con una marca de tiempo en UTC, un nivel, el nombre del módulo, el mensaje y campos de contexto. Cada ejecución tendría un `run_id` único.

| Nivel | Información que registraría |
|---|---|
| DEBUG | Identificador de fila, número de bloque, trabajador que procesa el registro, valores de control necesarios para seguir las transformaciones y orden de procesamiento. Se puede activar detalladamente durante la investigación. |
| INFO | Inicio y final de cada ejecución, nombre del archivo, hash SHA-256, configuración, versiones de Python y dependencias, cantidad de filas leídas, procesadas y escritas, y duración de cada etapa. |
| WARNING | Filas duplicadas, valores nulos, registros descartados, conversiones inesperadas, reintentos y diferencias respecto a las cantidades esperadas. |
| ERROR | Inconsistencias detectadas en las validaciones, cantidades incorrectas, resultados incompletos y fallos de lectura o escritura. Registraría también el contexto de la etapa y el identificador de ejecución, aunque no exista una excepción. |
| CRITICAL | Una condición que impida garantizar la integridad del resultado, como una salida incompleta que no pueda recuperarse. Registraría el motivo y la acción de interrupción. |

Además, definiría validaciones explícitas antes de finalizar:

- La cantidad de filas leídas debe coincidir con la cantidad procesada más las filas descartadas justificadamente.
- Las columnas obligatorias deben existir.
- Los identificadores que deban ser únicos no deben presentar duplicados.
- La cantidad de registros escritos debe coincidir con la cantidad esperada.
- El archivo final debe estar completo y poder leerse nuevamente.

Si una validación falla, registraría un evento `ERROR` con los valores esperados y obtenidos, el `run_id` y la etapa correspondiente. No registraría indiscriminadamente datos personales o información sensible del CSV.

### 3.4. Limitaciones de los puntos de interrupción

Un depurador con puntos de interrupción tampoco es la primera herramienta adecuada porque detiene la ejecución en momentos específicos. Si el fallo depende de una condición de carrera, la pausa puede alterar la planificación de los hilos y modificar el comportamiento que se intenta investigar.

Además, detener una ejecución no garantiza capturar el estado exacto que produjo el resultado incorrecto. Como el problema aparece aproximadamente en una de cada veinte ejecuciones, inspeccionar una ejecución que funciona no permite concluir que el defecto esté resuelto.

Un punto de interrupción sí sería adecuado cuando el problema sea reproducible de forma determinista, exista una ubicación concreta sospechosa y se necesite inspeccionar paso a paso los valores de las variables, las condiciones y la pila de llamadas.

### 3.5. Estrategia para forzar la reproducibilidad

Implementaría un procedimiento de pruebas repetidas y controladas:

1. Guardar una copia inmutable del CSV original y calcular su hash SHA-256.
2. Fijar la versión de Python, las dependencias, la configuración, la codificación y los parámetros del procesamiento.
3. Registrar la semilla aleatoria cuando el programa utilice operaciones aleatorias.
4. Ejecutar repetidamente el procesamiento con exactamente los mismos datos, primero de forma secuencial y después con el nivel de concurrencia habitual.
5. Guardar cada resultado en un archivo independiente y calcular su hash SHA-256 para detectar diferencias.
6. Registrar el `run_id`, el número de filas, la duración, los trabajadores utilizados y las validaciones de cada ejecución.
7. Cuando aparezca una diferencia, conservar el CSV, la configuración, los registros y los resultados de esa ejecución para analizarla sin depender de que el fallo vuelva a ocurrir.

Un ejemplo de automatización en Bash para repetir el procesamiento es:

```bash
for i in $(seq 1 1000); do
    echo "Ejecución $i"
    python main.py datos.csv --output "resultados/salida_$i.csv" || break
done
```

Este comando es una plantilla: los argumentos `datos.csv` y `--output` deben adaptarse a la interfaz real del script. La carpeta `resultados/` debe existir previamente.

Después de las ejecuciones compararía los hashes de las salidas y revisaría los registros de las ejecuciones diferentes. Si el fallo se relaciona con concurrencia, también repetiría la prueba variando el número de trabajadores y el tamaño de los bloques para identificar qué condición lo desencadena.

**Limitación y siguiente investigación:** sin disponer del código fuente del procesador CSV ni de una ejecución que produzca el resultado incorrecto, no es posible afirmar cuál de las hipótesis es la causa real. Hasta aquí se establece un procedimiento verificable para aislar el problema. Para determinar la causa definitiva todavía habría que inspeccionar el código y contrastar los registros de una ejecución fallida con los de una ejecución correcta.


cat >> parcial1/respuestas.md <<'EOF'

## Pregunta 4. Perfilamiento y optimización del rendimiento

### 4.1. Identificación de los dos cuellos de botella

El tiempo total informado por el perfilador es de 84.112 segundos. Para identificar los cuellos de botella, comparo el tiempo propio (`tottime`) de las funciones que consumen más tiempo y calculo su porcentaje respecto al tiempo total.

**Primer cuello de botella: `normalizar_texto`.**

Esta función se ejecuta 240.000 veces y consume 41.900 segundos de tiempo propio.

Operación:

\[
\frac{41.900}{84.112}\times 100 \approx 49.81\%
\]

Por tanto, la normalización de texto representa aproximadamente el 49.81 % del tiempo total.

**Segundo cuello de botella: `comparar_lineal`.**

Esta función consume 37.390 segundos de tiempo propio y se ejecuta dentro de las búsquedas en el catálogo.

Operación:

\[
\frac{37.390}{84.112}\times 100 \approx 44.45\%
\]

Por tanto, la comparación lineal representa aproximadamente el 44.45 % del tiempo total.

Las dos funciones concentran aproximadamente el 94.26 % del tiempo medido:

\[
49.81\%+44.45\%=94.26\%
\]

La optimización debe priorizar estas funciones, especialmente la comparación lineal porque permite cambiar el mecanismo de búsqueda y reducir su costo asintótico.

### 4.2. Diferencia entre tottime y cumtime

`tottime` es el tiempo empleado directamente dentro de una función, sin incluir el tiempo consumido por las funciones que esta llama.

`cumtime` es el tiempo acumulado de una función, incluyendo el tiempo de sus llamadas internas.

En la tabla, `buscar_en_catalogo` presenta:

- `tottime`: 1.210 segundos.
- `cumtime`: 38.600 segundos.

Esto significa que la función utiliza directamente 1.210 segundos, pero el tiempo total asociado a su ejecución asciende a 38.600 segundos porque también ejecuta otras funciones.

Una de ellas es `comparar_lineal`, que consume 37.390 segundos:

\[
1.210+37.390=38.600
\]

La operación coincide exactamente con el `cumtime` de `buscar_en_catalogo`.

Por eso su `tottime` es bajo y su `cumtime` es alto: la mayor parte del tiempo no se consume en el código propio de búsqueda, sino en la función interna que compara linealmente los elementos.

No deben sumarse los 38.600 segundos de `buscar_en_catalogo` y los 37.390 segundos de `comparar_lineal` como si fueran costos independientes, porque se estaría contando dos veces el tiempo de la comparación.

### 4.3. Optimización de comparar_lineal

Reemplazaría la búsqueda lineal por una estructura de datos basada en tablas hash de Python.

Si el programa necesita comprobar si un elemento existe en el catálogo, utilizaría un `set`. Si necesita recuperar información asociada a una clave, utilizaría un diccionario (`dict`).

Por ejemplo, para búsquedas por identificador:

```python
# Construcción del índice una sola vez.
catalogo_por_id = {
    elemento["id"]: elemento
    for elemento in catalogo
}

# Búsqueda por identificador.
resultado = catalogo_por_id.get(id_buscado)
```

Este ejemplo supone que `id` es una clave única y que la búsqueda original se realiza por ese identificador. Si existen identificadores repetidos, habría que conservar la regla original de selección, por ejemplo, almacenando una lista de elementos por identificador. Si la comparación original utiliza otra clave, el índice debe construirse con esa misma clave.

**Complejidad antes de la optimización:**

Si existen N registros que deben consultarse y M elementos en el catálogo, una búsqueda lineal puede recorrer hasta M elementos por cada consulta.
\[
T(N,M)=O(N\times M)
\]

En el peor caso, cada consulta revisa todo el catálogo.

**Complejidad después de la optimización:**

La construcción del diccionario requiere recorrer el catálogo una vez: \(O(M)\).

Después, las consultas tienen un costo promedio de \(O(1)\) por búsqueda mediante una tabla hash.

Por tanto:
\[
T(N,M)=O(M+N)
\]

Esta complejidad es promedio; en casos extremos de colisiones, las operaciones de una tabla hash pueden ser más costosas.

La optimización también requiere memoria adicional para almacenar el índice. Además, hay que mantener las mismas reglas de comparación, normalización y tratamiento de identificadores para no cambiar el resultado funcional del programa.

**Estimación del nuevo tiempo total:**

Como primera estimación, supongo que la optimización elimina los 37.390 segundos consumidos por comparar_lineal y que el costo de construir el índice es pequeño frente al tiempo medido.
\[
T_{\text{nuevo}}=84.112-37.390
\]

\[
\boxed{T_{\text{nuevo}}\approx46.722\text{ segundos}}
\]

La reducción estimada es de 37.390 segundos, equivalente aproximadamente al 44.45 % del tiempo original.

Esta cifra es una estimación teórica basada en el perfil suministrado, no un resultado de una ejecución posterior. El tiempo real debe medirse después de implementar la optimización, incluyendo la construcción del índice y verificando que los resultados sean correctos.
### 4.4. Nuevo cuello de botella después de optimizar
Al eliminar el costo de `comparar_lineal`, la función que pasa a representar la mayor proporción del tiempo es `normalizar_texto`, que conserva sus 41.900 segundos de tiempo propio.

Utilizando el nuevo tiempo total estimado:
\[
\frac{41.900}{46.722}\times100\approx89.68\%
\]

Por tanto, `normalizar_texto` representaría aproximadamente el 89.68 % del nuevo tiempo total.

Esto demuestra que optimizar una función puede cambiar completamente la distribución del tiempo de ejecución. Después de mejorar la búsqueda, la siguiente prioridad sería investigar la normalización de texto: operaciones repetidas, expresiones regulares, conversiones innecesarias y trabajo que pueda reutilizarse mediante almacenamiento en caché cuando sea correcto hacerlo.
### 4.5. Por qué no paralelizar `leer_archivo`
No paralelizaría `leer_archivo` como primera medida porque los datos del perfilador muestran que consume solamente 2.100 segundos de los 84.112 segundos totales.

Su porcentaje es:
\[
\frac{2.100}{84.112}\times100\approx2.50\%
\]

En cambio, normalizar_texto consume aproximadamente el 49.81 % y comparar_lineal el 44.45 %. Por tanto, la lectura del archivo no es el principal problema de rendimiento identificado.

Incluso en el supuesto ideal de eliminar completamente el tiempo de lectura, la mejora máxima sería de 2.100 segundos, aproximadamente el 2.50 % del tiempo original. En la práctica, paralelizar puede introducir costos adicionales de coordinación, transferencia de datos, sincronización y administración de trabajadores.

El principio que se debe aplicar es la ley de Amdahl: la mejora global está limitada por la proporción del programa que realmente se optimiza. También debe aplicarse el principio de perfilar antes de optimizar: las decisiones deben basarse en mediciones y no en suposiciones generales sobre qué parte del programa es lenta.

La decisión correcta es optimizar primero las funciones que concentran el tiempo medido y volver a perfilar después de cada cambio. Solo consideraría paralelizar la lectura si nuevas mediciones demostraran que se ha convertido en un cuello de botella significativo.

Alcance de la conclusión: los porcentajes y la estimación se calculan con los datos suministrados por el enunciado. No se dispone del código fuente ni de una ejecución optimizada para verificar el tiempo real posterior. Por eso, los 46.722 segundos son una estimación bajo los supuestos indicados, no una medición experimental.
EOF