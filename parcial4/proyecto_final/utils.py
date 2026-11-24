MONEDAS_DISPONIBLES = {"USD", "EUR", "COP"}


def parsear_monto(texto):
    """Convierte el texto ingresado en un monto positivo."""
    try:
        monto = float(texto)
    except (TypeError, ValueError):
        raise ValueError("Debe ingresar un número válido.")

    if monto <= 0:
        raise ValueError("El monto debe ser mayor que cero.")

    return monto


def validar_monto(monto):
    """Indica si el monto es positivo."""
    return monto > 0


def formatear_monto(monto):
    """Devuelve el monto con dos decimales y separador de miles."""
    return "{:,.2f}".format(monto)
