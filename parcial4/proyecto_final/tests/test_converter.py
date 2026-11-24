import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from converter import (
    cargar_tasas_csv,
    convertir_monto,
    obtener_tasas_api,
)
from utils import formatear_monto, parsear_monto, validar_monto


class TestConversor(unittest.TestCase):

    def test_parsear_monto_texto_invalido(self):
        with self.assertRaisesRegex(ValueError, "número válido"):
            parsear_monto("hola")

    def test_rechazar_monto_negativo(self):
        with self.assertRaisesRegex(ValueError, "mayor que cero"):
            parsear_monto("-25")

    def test_validar_monto_positivo(self):
        self.assertTrue(validar_monto(100))
        self.assertFalse(validar_monto(-1))

    def test_convertir_usd_a_eur(self):
        resultado = convertir_monto(
            100,
            "USD",
            "EUR",
            {"EUR": 0.92},
        )
        self.assertAlmostEqual(resultado, 92.0)

    def test_convertir_a_la_misma_moneda(self):
        resultado = convertir_monto(
            50,
            "COP",
            "COP",
            {},
        )
        self.assertEqual(resultado, 50)

    def test_rechazar_moneda_sin_tasa(self):
        with self.assertRaisesRegex(ValueError, "No existe una tasa"):
            convertir_monto(100, "USD", "EUR", {})

    def test_cargar_tasas_desde_csv(self):
        contenido = (
            "moneda_base,moneda_destino,tasa\n"
            "USD,EUR,0.92\n"
            "USD,COP,4200.00\n"
            "EUR,USD,1.09\n"
        )

        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "tasas.csv"
            ruta.write_text(contenido, encoding="utf-8")

            tasas = cargar_tasas_csv(ruta, "USD")

        self.assertEqual(tasas, {"EUR": 0.92, "COP": 4200.0})

    @patch("converter.requests.get")
    def test_consultar_api_con_respuesta_simulada(self, solicitud_mock):
        respuesta = Mock()
        respuesta.json.return_value = {"rates": {"EUR": 0.95}}
        respuesta.raise_for_status.return_value = None
        solicitud_mock.return_value = respuesta

        tasas = obtener_tasas_api(
            "https://api.ejemplo.test/latest",
            "CLAVE_DE_PRUEBA",
            "USD",
        )

        self.assertEqual(tasas, {"EUR": 0.95})
        solicitud_mock.assert_called_once()

    @patch("converter.requests.get")
    def test_api_no_disponible_devuelve_none(self, solicitud_mock):
        import requests

        solicitud_mock.side_effect = requests.exceptions.Timeout

        tasas = obtener_tasas_api(
            "https://api.ejemplo.test/latest",
            "CLAVE_DE_PRUEBA",
            "USD",
        )

        self.assertIsNone(tasas)

    def test_formatear_monto(self):
        self.assertEqual(formatear_monto(1250.5), "1,250.50")


if __name__ == "__main__":
    unittest.main()
