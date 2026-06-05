import subprocess
import sys
import os
from price_manager.database.connection import session_scope
from price_manager.models.models import PrecioCompetencia

class ScraperService:
    @staticmethod
    def ejecutar_scraping() -> bool:
        """Ejecuta el crawler de Scrapy como un subproceso para evitar conflictos con Twisted."""
        print("\n[INFO] Iniciando el proceso de scraping web en starcomputacion.com.ar...")
        
        # Vaciar la tabla de competencia previa
        with session_scope() as session:
            try:
                session.query(PrecioCompetencia).delete()
            except Exception as e:
                print(f"Advertencia al limpiar base de datos: {e}")

        # Ruta del script de ejecución del spider
        current_dir = os.path.dirname(os.path.abspath(__file__))
        run_spider_path = os.path.abspath(os.path.join(current_dir, "..", "scraper", "run_spider.py"))

        # Ejecutar el subproceso
        result = subprocess.run([sys.executable, run_spider_path], capture_output=True, text=True)

        if result.returncode == 0:
            print("[OK] Scraping finalizado con exito.")
            with session_scope() as session:
                cantidad = session.query(PrecioCompetencia).count()
                print(f"[STATS] Se registraron {cantidad} cotizaciones de la competencia en la base de datos.")
            return True
        else:
            print("[ERROR] Ocurrio un error al ejecutar el scraping:")
            print(result.stderr)
            print(result.stdout)
            return False
