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
