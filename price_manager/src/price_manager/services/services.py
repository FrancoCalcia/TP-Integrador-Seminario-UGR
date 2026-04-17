from datetime import date
from typing import List

from price_manager.entities.entities import (
  Producto,
  Precio,
  Stock,
  CotizacionDolar,
)

from price_manager.repositories.repositories import (
  RepositorioProducto,
  RepositorioStock,
  RepositorioCotizacionDolar,
)


# SERVICIO PRODUCTO

class ServicioProducto:

  def __init__(self, repo_producto: RepositorioProducto) -> None:
    self.repo = repo_producto

  def crear_producto(
      self,
      id: int,
      nombre: str,
      descripcion: str,
      valor: float,
      moneda,
      categoria,
      proveedor,
  ) -> Producto:

    if valor <= 0:
      raise ValueError("El precio debe ser mayor a 0.")

    precio = Precio(valor, moneda, date.today())

    producto = Producto(
      id,
      nombre,
      descripcion,
      precio,
      categoria,
      proveedor,
    )

    return self.repo.crear(producto)

  def obtener_producto(self, id: int) -> Producto:
    producto = self.repo.leer_por_id(id)
    if not producto:
      raise ValueError("Producto no encontrado.")
    return producto

  def listar_productos(self) -> List[Producto]:
    return self.repo.leer_todos()

  def actualizar_precio(
      self,
      id: int,
      nuevo_valor: float,
      nueva_moneda,
  ) -> Producto:

    if nuevo_valor <= 0:
      raise ValueError("El precio debe ser mayor a 0.")

    producto = self.obtener_producto(id)

    producto.precio = Precio(
      nuevo_valor,
      nueva_moneda,
      date.today()
    )

    return self.repo.actualizar(producto)

  def eliminar_producto(self, id: int) -> bool:
    return self.repo.eliminar(id)


# SERVICIO STOCK

class ServicioStock:

  def __init__(self, repo_stock: RepositorioStock) -> None:
    self.repo = repo_stock

  def crear_stock(self, stock: Stock) -> Stock:
    return self.repo.crear(stock)

  def obtener_stock(self, producto_id: int) -> Stock:
    stock = self.repo.leer_por_producto(producto_id)
    if not stock:
      raise ValueError("Stock no encontrado.")
    return stock

  def listar_stock(self) -> List[Stock]:
    return self.repo.leer_todos()

  def actualizar_stock(self, stock: Stock) -> Stock:
    return self.repo.actualizar(stock)

  def eliminar_stock(self, producto_id: int) -> bool:
    return self.repo.eliminar(producto_id)


# SERVICIO COTIZACION

class ServicioCotizacion:

  def __init__(
      self,
      repo_cotizacion: RepositorioCotizacionDolar
  ) -> None:
    self.repo = repo_cotizacion

  def crear_cotizacion(
      self,
      cotizacion: CotizacionDolar
  ) -> CotizacionDolar:
    return self.repo.crear(cotizacion)

  def obtener_cotizacion(
      self,
      tipo_id: int,
      fecha
  ) -> CotizacionDolar:
    cotizacion = self.repo.leer_por_tipo_y_fecha(tipo_id, fecha)
    if not cotizacion:
      raise ValueError("Cotizacion no encontrada.")
    return cotizacion

  def listar_cotizaciones(self) -> List[CotizacionDolar]:
    return self.repo.leer_todos()

  def actualizar_cotizacion(
      self,
      cotizacion: CotizacionDolar
  ) -> CotizacionDolar:
    return self.repo.actualizar(cotizacion)

  def eliminar_cotizacion(
      self,
      tipo_id: int,
      fecha
  ) -> bool:
    return self.repo.eliminar(tipo_id, fecha)