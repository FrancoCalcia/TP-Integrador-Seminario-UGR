import os
import csv
from datetime import datetime
from pathlib import Path
import pandas as pd

from price_manager.database.connection import session_scope
from price_manager.models.models import Producto, PrecioCompetencia, CotizacionDolar

class ReportService:
    @staticmethod
    def get_paths():
        """Retorna las rutas para guardar alertas y reportes según el entorno."""
        if os.path.exists('/content'):
            alerts_dir = "/content/TP-Integrador-Seminario-UGR/price_manager/alerts"
            reports_dir = "/content/TP-Integrador-Seminario-UGR/price_manager"
        else:
            # En local, relativo a la carpeta raíz del proyecto
            project_root = Path(__file__).resolve().parents[3]
            alerts_dir = str(project_root / "price_manager" / "alerts")
            reports_dir = str(project_root / "price_manager")
        
        os.makedirs(alerts_dir, exist_ok=True)
        return alerts_dir, reports_dir

    @classmethod
    def generar_alerta_csv(cls, diferencia_limite: float) -> str:
        """Compara precios y genera un archivo CSV de alerta si superan el límite."""
        alerts_dir, _ = cls.get_paths()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"alert_{timestamp}.csv"
        csv_path = os.path.join(alerts_dir, csv_filename)

        alertas = []

        with session_scope() as session:
            # Obtener cotización del dólar blue para conversiones si es necesario
            latest_blue = session.query(CotizacionDolar).filter(
                CotizacionDolar.nombre.like('%Blue%')
            ).order_by(CotizacionDolar.fecha_actualizacion.desc()).first()
            usd_blue = latest_blue.venta if latest_blue else 1000.0

            # Obtener cotizaciones de competencia
            competencia = session.query(PrecioCompetencia).all()

            for pc in competencia:
                prod = session.query(Producto).filter(Producto.id == pc.producto_interno_id).first()
                if not prod or not prod.precio:
                    continue

                # Convertir precio interno a ARS si está en USD
                precio_interno_ars = prod.precio.valor
                if prod.precio.moneda.upper() == 'USD':
                    precio_interno_ars = prod.precio.valor * usd_blue

                diferencia = abs(precio_interno_ars - pc.precio_web)

                if diferencia > diferencia_limite:
                    alertas.append({
                        'Producto': prod.nombre,
                        'Precio Interno': f"{precio_interno_ars:.2f}",
                        'Precio Web': f"{pc.precio_web:.2f}",
                        'Diferencia': f"{diferencia:.2f}",
                        'Fecha de extraccion': pc.fecha_extraccion.strftime("%Y-%m-%d %H:%M:%S")
                    })

        if not alertas:
            print("[INFO] No se encontraron diferencias que superen el limite de alerta ingresado.")
            return ""

        # Escribir el CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Producto', 'Precio Interno', 'Precio Web', 'Diferencia', 'Fecha de extraccion']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for al in alertas:
                writer.writerow(al)

        print(f"[ALERTA] Alertas guardadas en: {csv_path}")
        return csv_path

    @classmethod
    def generar_reporte_excel(cls) -> str:
        """Genera el reporte de precios comparativos en formato Excel (.xlsx)."""
        _, reports_dir = cls.get_paths()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = f"report_{timestamp}.xlsx"
        excel_path = os.path.join(reports_dir, excel_filename)

        datos = []

        with session_scope() as session:
            latest_blue = session.query(CotizacionDolar).filter(
                CotizacionDolar.nombre.like('%Blue%')
            ).order_by(CotizacionDolar.fecha_actualizacion.desc()).first()
            usd_blue = latest_blue.venta if latest_blue else 1000.0

            competencia = session.query(PrecioCompetencia).all()

            for pc in competencia:
                prod = session.query(Producto).filter(Producto.id == pc.producto_interno_id).first()
                if not prod or not prod.precio:
                    continue

                precio_interno_ars = prod.precio.valor
                if prod.precio.moneda.upper() == 'USD':
                    precio_interno_ars = prod.precio.valor * usd_blue

                diferencia = abs(precio_interno_ars - pc.precio_web)

                datos.append({
                    'Producto': prod.nombre,
                    'Precio interno': round(precio_interno_ars, 2),
                    'Precio web': round(pc.precio_web, 2),
                    'Diferencia': round(diferencia, 2),
                    'Fecha de extracción': pc.fecha_extraccion.strftime("%Y-%m-%d %H:%M:%S")
                })

        if not datos:
            print("[INFO] No hay datos de competencia guardados para generar el reporte. Por favor, ejecute el scraping primero.")
            return ""

        # Generar Excel con pandas
        df = pd.DataFrame(datos)
        df.to_excel(excel_path, index=False)
        print(f"[REPORTE] Reporte excel generado correctamente en: {excel_path}")
        return excel_path
