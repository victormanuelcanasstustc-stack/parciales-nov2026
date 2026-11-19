#!/usr/bin/env bash

# Mostrar los 10 archivos mas grandes de una carpeta.
# Se usan registros terminados en NUL para preservar nombres con espacios.

find parcial1/archivos_prueba -type f -printf '%s\t%p\0' |
sort -z -t $'\t' -k1,1nr |
head -z -n 10 |
while IFS= read -r -d '' registro; do
    size="${registro%%$'\t'*}"
    archivo="${registro#*$'\t'}"
    printf "%8s bytes  %s\n" "$size" "$archivo"
done
