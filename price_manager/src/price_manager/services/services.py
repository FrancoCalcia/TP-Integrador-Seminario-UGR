from typing import List
from datetime import date

from price_manager.entities.entities import (
  Producto, Precio, Stock, CotizacionDolar
)


# SERVICIOS SIMPLES (CRUD)

class ServicioCategoria:

  def __init__(self, repo):
    self.repo = repo

  def crear(self, entidad):
    return self.repo.crear(entidad)

  def obtener(self, id):
    obj = self.repo.leer_por_id(id)
    if not obj:
      raise ValueError("Categoria no encontrada")
    return obj

  def listar_todos(self):
    return self.repo.leer_todos()

  def actualizar(self, entidad):
    return self.repo.actualizar(entidad)

  def eliminar(self, id):
    if not self.repo.eliminar(id):
      raise ValueError("Categoria no encontrada")


class ServicioProveedor:

  def __init__(self, repo):
    self.repo = repo

  def crear(self, entidad):
    return self.repo.crear(entidad)

  def obtener(self, id):
    obj = self.repo.leer_por_id(id)
    if not obj:
      raise ValueError("Proveedor no encontrado")
    return obj

  def listar_todos(self):
    return self.repo.leer_todos()

  def actualizar(self, entidad):
    return self.repo.actualizar(entidad)

  def eliminar(self, id):
    if not self.repo.eliminar(id):
      raise ValueError("Proveedor no encontrado")


class ServicioMoneda:

  def __init__(self, repo):
    self.repo = repo

  def crear(self, entidad):
    return self.repo.crear(entidad)

  def obtener(self, id):
    obj = self.repo.leer_por_id(id)
    if not obj:
      raise ValueError("Moneda no encontrada")
    return obj

  def listar_todos(self):
    return self.repo.leer_todos()

  def actualizar(self, entidad):
    return self.repo.actualizar(entidad)

  def eliminar(self, id):
    if not self.repo.eliminar(id):
      raise ValueError("Moneda no encontrada")


class ServicioTipoCotizacion:

  def __init__(self, repo):
    self.repo = repo

  def crear(self, entidad):
    return self.repo.crear(entidad)

  def obtener(self, id):
    obj = self.repo.leer_por_id(id)
    if not obj:
      raise ValueError("TipoCotizacion no encontrado")
    return obj

  def listar_todos(self):
    return self.repo.leer_todos()

  def actualizar(self, entidad):
    return self.repo.actualizar(entidad)

  def eliminar(self, id):
    if not self.repo.eliminar(id):
      raise ValueError("TipoCotizacion no encontrado")


# SERVICIO PRODUCTO

class ServicioProducto:

  def __init__(self, repo_producto, srv_categoria, srv_proveedor):
    self.repo = repo_producto
    self.srv_categoria = srv_categoria
    self.srv_proveedor = srv_proveedor

  def crear(self, producto: Producto) -> Producto:
    return self.repo.crear(producto)

  def obtener(self, id: int) -> Producto:
    producto = self.repo.leer_por_id(id)
    if not producto:
      raise ValueError("Producto no encontrado")
    return producto

  def listar_todos(self) -> List[Producto]:
    return self.repo.leer_todos()

  def actualizar(self, producto: Producto) -> Producto:
    return self.repo.actualizar(producto)

  def eliminar(self, id: int):
    if not self.repo.eliminar(id):
      raise ValueError("Producto no encontrado")


# SERVICIO STOCK

class ServicioStock:

  def __init__(self, repo_stock, srv_producto):
    self.repo = repo_stock
    self.srv_producto = srv_producto

  def registrar_movimiento(self, producto_id: int, cantidad: int):

    # Validar producto
    producto = self.srv_producto.obtener(producto_id)

    stock = self.repo.leer_por_producto(producto_id)

    if not stock:
      stock = Stock(producto, 0)

    nueva_cantidad = stock.cantidad + cantidad

    if nueva_cantidad < 0:
      raise ValueError("Stock no puede ser negativo")

    stock.cantidad = nueva_cantidad

    if self.repo.leer_por_producto(producto_id):
      self.repo.actualizar(stock)
    else:
      self.repo.crear(stock)

  def obtener_stock(self, producto_id: int) -> int:
    stock = self.repo.leer_por_producto(producto_id)
    return stock.cantidad if stock else 0


# SERVICIO COTIZACION

class ServicioCotizacionDolar:

  def __init__(self, repo_cotizacion, srv_tipo):
    self.repo = repo_cotizacion
    self.srv_tipo = srv_tipo

  def registrar_cotizacion(self, cotizacion: CotizacionDolar):
    return self.repo.crear(cotizacion)

  def listar_todas(self):
    return self.repo.leer_todos()

  def actualizar_cotizacion(self, cotizacion: CotizacionDolar):
    return self.repo.actualizar(cotizacion)

  def eliminar_cotizacion(self, tipo_id: int, fecha):
    if not self.repo.eliminar(tipo_id, fecha):
      raise ValueError("Cotizacion no encontrada")

  def obtener_historico(self, tipo_id: int):

    tipo = self.srv_tipo.obtener(tipo_id)

    historico = self.repo.leer_historico_por_tipo(tipo_id)

    if not historico:
      raise ValueError("No hay cotizaciones para este tipo")

    return historico