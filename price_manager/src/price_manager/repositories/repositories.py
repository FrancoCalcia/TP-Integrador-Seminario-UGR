import abc
import datetime
import sys
from pathlib import Path
from typing import Dict, Generic, List, Optional, Tuple, TypeVar

SRC_PATH = Path(__file__).resolve().parents[2]
if str(SRC_PATH) not in sys.path:
  sys.path.insert(0, str(SRC_PATH))

from price_manager.entities.entities import (
  Categoria,
  CotizacionDolar,
  EntidadBase,
  Moneda,
  Producto,
  Proveedor,
  Stock,
  TipoCotizacion,
)


T = TypeVar("T", bound=EntidadBase)


class IRepositorio(abc.ABC, Generic[T]):
  """Interfaz para repositorios con operaciones CRUD basicas."""

  @abc.abstractmethod
  def crear(self, entidad: T) -> T:
    """Crea una entidad nueva."""
    pass

  @abc.abstractmethod
  def leer_por_id(self, id: int) -> Optional[T]:
    """Busca una entidad por identificador."""
    pass

  @abc.abstractmethod
  def leer_todos(self) -> List[T]:
    """Devuelve todas las entidades guardadas."""
    pass

  @abc.abstractmethod
  def actualizar(self, entidad: T) -> T:
    """Actualiza una entidad existente."""
    pass

  @abc.abstractmethod
  def eliminar(self, id: int) -> bool:
    """Elimina una entidad por identificador."""
    pass


class IRepositorioStock(abc.ABC):
  """Interfaz para repositorios de stock."""

  @abc.abstractmethod
  def crear(self, stock: Stock) -> Stock:
    """Crea un registro de stock."""
    pass

  @abc.abstractmethod
  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
    """Busca el stock asociado a un producto."""
    pass

  @abc.abstractmethod
  def leer_todos(self) -> List[Stock]:
    """Devuelve todos los registros de stock."""
    pass

  @abc.abstractmethod
  def actualizar(self, stock: Stock) -> Stock:
    """Actualiza un registro de stock."""
    pass

  @abc.abstractmethod
  def eliminar(self, producto_id: int) -> bool:
    """Elimina el stock asociado a un producto."""
    pass


class IRepositorioCotizacionDolar(abc.ABC):
  """Interfaz para repositorios de cotizaciones del dolar."""

  @abc.abstractmethod
  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    """Crea una cotizacion."""
    pass

  @abc.abstractmethod
  def leer_por_tipo_y_fecha(
      self,
      tipo_id: int,
      fecha: datetime.date,
  ) -> Optional[CotizacionDolar]:
    """Busca una cotizacion por tipo y fecha."""
    pass

  @abc.abstractmethod
  def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
    """Devuelve el historico de cotizaciones de un tipo."""
    pass

  @abc.abstractmethod
  def leer_todos(self) -> List[CotizacionDolar]:
    """Devuelve todas las cotizaciones guardadas."""
    pass

  @abc.abstractmethod
  def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    """Actualiza una cotizacion existente."""
    pass

  @abc.abstractmethod
  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    """Elimina una cotizacion por tipo y fecha."""
    pass


class RepositorioMemoria(IRepositorio[T]):
  """Repositorio generico en memoria para entidades con id."""

  def __init__(self) -> None:
    self._datos: Dict[int, T] = {}

  def crear(self, entidad: T) -> T:
    if entidad.id in self._datos:
      raise ValueError(f"Ya existe una entidad con id {entidad.id}.")
    self._datos[entidad.id] = entidad
    return entidad

  def leer_por_id(self, id: int) -> Optional[T]:
    return self._datos.get(id)

  def leer_todos(self) -> List[T]:
    return list(self._datos.values())

  def actualizar(self, entidad: T) -> T:
    if entidad.id not in self._datos:
      raise ValueError(f"No existe una entidad con id {entidad.id}.")
    self._datos[entidad.id] = entidad
    return entidad

  def eliminar(self, id: int) -> bool:
    if id not in self._datos:
      return False
    del self._datos[id]
    return True


class RepositorioCategoria(RepositorioMemoria[Categoria]):
  """Repositorio de categorias."""


class RepositorioProveedor(RepositorioMemoria[Proveedor]):
  """Repositorio de proveedores."""


class RepositorioMoneda(RepositorioMemoria[Moneda]):
  """Repositorio de monedas."""


class RepositorioTipoCotizacion(RepositorioMemoria[TipoCotizacion]):
  """Repositorio de tipos de cotizacion."""


class RepositorioProducto(RepositorioMemoria[Producto]):
  """Repositorio de productos."""


class RepositorioStock(IRepositorioStock):
  """Repositorio en memoria de stock por producto."""

  def __init__(self) -> None:
    self._datos: Dict[int, Stock] = {}

  def crear(self, stock: Stock) -> Stock:
    if stock.producto_id in self._datos:
      raise ValueError(
        f"Ya existe stock para el producto {stock.producto_id}."
      )
    self._datos[stock.producto_id] = stock
    return stock

  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
    return self._datos.get(producto_id)

  def leer_todos(self) -> List[Stock]:
    return list(self._datos.values())

  def actualizar(self, stock: Stock) -> Stock:
    if stock.producto_id not in self._datos:
      raise ValueError(
        f"No existe stock para el producto {stock.producto_id}."
      )
    self._datos[stock.producto_id] = stock
    return stock

  def eliminar(self, producto_id: int) -> bool:
    if producto_id not in self._datos:
      return False
    del self._datos[producto_id]
    return True


class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
  """Repositorio en memoria de cotizaciones por tipo y fecha."""

  def __init__(self) -> None:
    self._datos: Dict[Tuple[int, datetime.date], CotizacionDolar] = {}

  def _crear_clave(
      self,
      tipo_id: int,
      fecha: datetime.date,
  ) -> Tuple[int, datetime.date]:
    return (tipo_id, fecha)

  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    clave = self._crear_clave(cotizacion.tipo.id, cotizacion.fecha)
    if clave in self._datos:
      raise ValueError("Ya existe una cotizacion para ese tipo y fecha.")
    self._datos[clave] = cotizacion
    return cotizacion

  def leer_por_tipo_y_fecha(
      self,
      tipo_id: int,
      fecha: datetime.date,
  ) -> Optional[CotizacionDolar]:
    return self._datos.get(self._crear_clave(tipo_id, fecha))

  def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
    historico = [
      cotizacion
      for (id_tipo, _), cotizacion in self._datos.items()
      if id_tipo == tipo_id
    ]
    return sorted(historico, key=lambda cotizacion: cotizacion.fecha)

  def leer_todos(self) -> List[CotizacionDolar]:
    return sorted(
      self._datos.values(),
      key=lambda cotizacion: (cotizacion.tipo.id, cotizacion.fecha),
    )

  def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    clave = self._crear_clave(cotizacion.tipo.id, cotizacion.fecha)
    if clave not in self._datos:
      raise ValueError("No existe una cotizacion para ese tipo y fecha.")
    self._datos[clave] = cotizacion
    return cotizacion

  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    clave = self._crear_clave(tipo_id, fecha)
    if clave not in self._datos:
      return False
    del self._datos[clave]
    return True
