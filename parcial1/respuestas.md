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