#!/usr/bin/env bash

# Buscar TODO en archivos Python modificados durante los ultimos 7 dias.

find parcial1/archivos_prueba \
  -type f \
  -name "*.py" \
  -mmin -10080 \
  -print0 |
xargs -0 -r grep -nH -- "TODO"
