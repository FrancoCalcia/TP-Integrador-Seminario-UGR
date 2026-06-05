import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from price_manager.database.connection import session_scope
from price_manager.models.models import CotizacionDolar

from pathlib import Path
if os.path.exists('/content'):
    load_dotenv("/content/TP-Integrador-Seminario-UGR/price_manager/.env")
else:
    load_dotenv(str(Path(__file__).resolve().parents[2] / ".env"))


class ServicioCotizacionDolar:
    def __init__(self):
        self.api_url = os.getenv('API_URL', 'https://dolarapi.com/v1/dolares')

    def obtener_cotizaciones(self):
        """Busca, descarga, guarda en BD y muestra las cotizaciones de la API."""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            print('--- Cotizaciones Actuales ---')
            with session_scope() as session:
                for moneda in data:
                    print(f"{moneda['nombre']}: Compra ${moneda['compra']} - Venta ${moneda['venta']}")
                    # Guardamos en base de datos
                    cotizacion = CotizacionDolar(
                        nombre=moneda['nombre'],
                        compra=moneda['compra'],
                        venta=moneda['venta'],
                        fecha_actualizacion=datetime.now()
                    )
                    session.add(cotizacion)
            return data
        except Exception as e:
            print(f'Error al obtener cotizaciones: {e}')
            return None
