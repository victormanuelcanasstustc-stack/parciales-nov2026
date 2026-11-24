import logging
import re

logger = logging.getLogger(__name__)

FORMATO_ESTANDAR = re.compile(
    r"^-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d{1,2})?$"
)

FORMATO_EUROPEO = re.compile(
    r"^-?\d{1,3}(?:\.\d{3})+,\d{1,2}$"
)


def convertir(fila):
    valor_original = fila.get("monto")

    if valor_original is None:
        raise ValueError("La fila no contiene el campo 'monto'")

    valor = str(valor_original).strip()

    if FORMATO_EUROPEO.fullmatch(valor):
        normalizado = valor.replace(".", "").replace(",", ".")
    elif FORMATO_ESTANDAR.fullmatch(valor):
        normalizado = valor.replace(",", "")
    else:
        logger.warning(
            "Se encontró un monto con formato inválido",
            extra={
                "evento": "monto_invalido",
                "campo": "monto",
                "valor": valor,
            },
        )
        raise ValueError(f"Formato de monto inválido: {valor!r}")

    try:
        return float(normalizado)
    except ValueError as error:
        logger.exception(
            "No fue posible convertir el monto",
            extra={"evento": "error_conversion", "valor": valor},
        )
        raise ValueError(
            f"No fue posible convertir el monto: {valor!r}"
        ) from error
