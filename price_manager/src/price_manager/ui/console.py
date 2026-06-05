import os
import csv
from pathlib import Path
from price_manager.services.services import ServicioCotizacionDolar
from price_manager.services.scraper_service import ScraperService
from price_manager.services.report_service import ReportService
from price_manager.database.connection import session_scope
from price_manager.repositories.repositories import ProductoRepository
from price_manager.models.models import Auditoria
from price_manager.utils.audit import auditar

class ConsoleUI:
    def __init__(self):
        self.servicio_dolar = ServicioCotizacionDolar()

    def mostrar_menu(self):
        while True:
            print("\n--- Price Manager - Menú ---")
            print("1. Obtener cotizaciones por API")
            print("2. Ver lista de precios bimonetaria")
            print("3. Exportar precios a CSV")
            print("4. Ejecutar scraping (Competencia)")
            print("5. Generar reporte comparativo e ingresar alertas")
            print("6. Ver historial de auditoría")
            print("0. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.obtener_cotizaciones_menu()
            elif opcion == "2":
                self.mostrar_precios_bimonetarios()
            elif opcion == "3":
                self.exportar_a_csv()
            elif opcion == "4":
                self.ejecutar_scraping_menu()
            elif opcion == "5":
                self.generar_reportes_menu()
            elif opcion == "6":
                self.ver_historial_auditoria()
            elif opcion == "0":
                break
            else:
                print("Opción no válida.")

    @auditar(accion="Obtener cotizaciones por API")
    def obtener_cotizaciones_menu(self):
        self.servicio_dolar.obtener_cotizaciones()

    @auditar(accion="Ejecutar Scraping")
    def ejecutar_scraping_menu(self):
        ScraperService.ejecutar_scraping()

    @auditar(accion="Generar Reporte y Alertas", detalle_func=lambda self: "Generacion de reporte excel y alertas CSV.")
    def generar_reportes_menu(self):
        # Primero generamos el reporte Excel
        excel_path = ReportService.generar_reporte_excel()
        if not excel_path:
            return
        
        # Luego solicitamos el límite de alerta
        try:
            limite = float(input("Ingrese la diferencia máxima permitida para generar alertas (ARS): "))
            csv_path = ReportService.generar_alerta_csv(limite)
            if csv_path:
                print(f"Alerta CSV creada en {csv_path} para diferencias superiores a ${limite:.2f}")
        except ValueError:
            print("Límite inválido. Se salta la generación de alerta CSV.")

    def ver_historial_auditoria(self):
        print("\n--- Historial de Auditoría ---")
        with session_scope() as session:
            logs = session.query(Auditoria).order_by(Auditoria.fecha.desc()).all()
            if not logs:
                print("No hay registros en el historial de auditoría.")
                return
            
            print(f"{'Acción':<30} | {'Fecha':<20} | {'Detalle'}")
            print("-" * 80)
            for log in logs:
                fecha_str = log.fecha.strftime("%Y-%m-%d %H:%M:%S")
                print(f"{log.accion:<30} | {fecha_str:<20} | {log.detalle}")

    def mostrar_precios_bimonetarios(self):
        """Muestra precios en ARS y una estimación en USD Blue."""
        cotizaciones = self.servicio_dolar.obtener_cotizaciones()
        usd_blue = next((c['venta'] for c in cotizaciones if 'Blue' in c['nombre']), 1000) if cotizaciones else 1000

        with session_scope() as session:
            repo = ProductoRepository(session)
            productos = repo.get_all()
            print(f"\n{'Producto':<20} | {'ARS':<10} | {'USD (est.)':<10}")
            print("-" * 45)
            for p in productos:
                precio_ars = p.precio.valor if p.precio else 0
                precio_usd = precio_ars / usd_blue if precio_ars else 0
                print(f"{p.nombre:<20} | ${precio_ars:<9.2f} | U$D {precio_usd:<8.2f}")

    def exportar_a_csv(self):
        """Exporta los productos y sus precios a un archivo CSV."""
        if os.path.exists('/content'):
            output_path = "/content/TP-Integrador-Seminario-UGR/price_manager/precios_exportados.csv"
        else:
            output_path = str(Path(__file__).resolve().parents[3] / "precios_exportados.csv")
            
        with session_scope() as session:
            repo = ProductoRepository(session)
            productos = repo.get_all()
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'nombre', 'precio', 'moneda', 'ultima_actualizacion']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for p in productos:
                    writer.writerow({
                        'id': p.id,
                        'nombre': p.nombre,
                        'precio': p.precio.valor if p.precio else 0,
                        'moneda': p.precio.moneda if p.precio else '',
                        'ultima_actualizacion': p.precio.ultima_actualizacion if p.precio else ''
                    })
        print(f"Precios exportados a: {output_path}")