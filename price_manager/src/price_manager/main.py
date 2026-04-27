import sys
from pathlib import Path


# GC: Esto acá lo pongo para poder ejecutar desde la raíz del proyecto sin problemas de importación :P
SRC_PATH = Path(__file__).resolve().parents[1]
if str(SRC_PATH) not in sys.path:
  sys.path.insert(0, str(SRC_PATH))

from price_manager.preload_data.preload_data import cargar_todos_los_datos
from price_manager.repositories.repositories import (
  RepositorioCategoria,
  RepositorioCotizacionDolar,
  RepositorioMoneda,
  RepositorioProducto,
  RepositorioProveedor,
  RepositorioStock,
  RepositorioTipoCotizacion,
)
from price_manager.services.services import (
  ServicioCategoria,
  ServicioCotizacionDolar,
  ServicioMoneda,
  ServicioProducto,
  ServicioProveedor,
  ServicioStock,
  ServicioTipoCotizacion,
)
from price_manager.ui.console import ConsoleApp


def build_application(import_default_data: bool = True) -> ConsoleApp:
  """Construye la aplicación con repositorios y servicios en memoria."""
  repo_cat = RepositorioCategoria()
  repo_prov = RepositorioProveedor()
  repo_mon = RepositorioMoneda()
  repo_tipo_cot = RepositorioTipoCotizacion()
  repo_prod = RepositorioProducto()
  repo_stock = RepositorioStock()
  repo_cot = RepositorioCotizacionDolar()

  srv_cat = ServicioCategoria(repo_cat)
  srv_prov = ServicioProveedor(repo_prov)
  srv_mon = ServicioMoneda(repo_mon)
  srv_tipo_cot = ServicioTipoCotizacion(repo_tipo_cot)
  srv_prod = ServicioProducto(repo_prod, srv_cat, srv_prov)
  srv_stock = ServicioStock(repo_stock, srv_prod)
  srv_cot = ServicioCotizacionDolar(repo_cot, srv_tipo_cot)

  if import_default_data:
    cargar_todos_los_datos(
      srv_cat,
      srv_prov,
      srv_mon,
      srv_tipo_cot,
      srv_prod,
      srv_stock,
      srv_cot,
    )

  return ConsoleApp(
    srv_categoria=srv_cat,
    srv_proveedor=srv_prov,
    srv_moneda=srv_mon,
    srv_tipo_cotizacion=srv_tipo_cot,
    srv_producto=srv_prod,
    srv_stock=srv_stock,
    srv_cotizacion=srv_cot,
  )


def main(import_default_data: bool = True) -> None:
  """Punto de entrada de la aplicación."""
  app = build_application(import_default_data=import_default_data)
  app.run()


if __name__ == "__main__":
  main(import_default_data=True)
