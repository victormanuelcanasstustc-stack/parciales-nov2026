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
