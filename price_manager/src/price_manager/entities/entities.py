import datetime


class EntidadBase:
  """Entidad base con identificador numerico positivo."""

  def __init__(self, id: int) -> None:
    self.id = id

  @property
  def id(self) -> int:
    return self._id

  @id.setter
  def id(self, value: int) -> None:
    if not isinstance(value, int) or value <= 0:
      raise ValueError("El id debe ser un numero entero positivo.")
    self._id = value


class Categoria(EntidadBase):
  """Rubro o clasificacion comercial de un producto."""

  def __init__(self, id: int, nombre: str) -> None:
    super().__init__(id)
    self.nombre = nombre

  @property
  def nombre(self) -> str:
    return self._nombre

  @nombre.setter
  def nombre(self, value: str) -> None:
    if not value or not value.strip():
      raise ValueError("El nombre de la categoria es obligatorio.")
    self._nombre = value.strip()


class Proveedor(EntidadBase):
  """Empresa o persona que provee mercaderia al negocio."""

  def __init__(self, id: int, nombre: str, contacto: str) -> None:
    super().__init__(id)
    self.nombre = nombre
    self.contacto = contacto

  @property
  def nombre(self) -> str:
    return self._nombre

  @nombre.setter
  def nombre(self, value: str) -> None:
    if not value or not value.strip():
      raise ValueError("El nombre del proveedor es obligatorio.")
    self._nombre = value.strip()

  @property
  def contacto(self) -> str:
    return self._contacto

  @contacto.setter
  def contacto(self, value: str) -> None:
    if not value or not value.strip():
      raise ValueError("El contacto del proveedor es obligatorio.")
    self._contacto = value.strip()


class Moneda(EntidadBase):
  """Moneda utilizada para expresar precios."""

  def __init__(self, id: int, nombre: str, codigo: str = "ARS") -> None:
    super().__init__(id)
    self.nombre = nombre
    self.codigo = codigo

  @property
  def nombre(self) -> str:
    return self._nombre

  @nombre.setter
  def nombre(self, value: str) -> None:
    if not value or not value.strip():
      raise ValueError("El nombre de la moneda es obligatorio.")
    self._nombre = value.strip()

  @property
  def codigo(self) -> str:
    return self._codigo

  @codigo.setter
  def codigo(self, value: str) -> None:
    codigo_normalizado = value.strip().upper() if value else ""
    if len(codigo_normalizado) != 3 or not codigo_normalizado.isalpha():
      raise ValueError("El codigo de moneda debe tener 3 letras.")
    self._codigo = codigo_normalizado


class TipoCotizacion(EntidadBase):
  """Tipo de cotizacion del dolar."""

  def __init__(self, id: int, nombre: str) -> None:
    super().__init__(id)
    self.nombre = nombre

  @property
  def nombre(self) -> str:
    return self._nombre

  @nombre.setter
  def nombre(self, value: str) -> None:
    if not value or not value.strip():
      raise ValueError("El nombre del tipo de cotizacion es obligatorio.")
    self._nombre = value.strip()


class Precio:
  """Valor monetario con moneda y fecha de actualizacion."""

  def __init__(
      self,
      valor: float,
      moneda: Moneda,
      fecha: datetime.date,
  ) -> None:
    self.valor = valor
    self.moneda = moneda
    self.fecha = fecha

  @property
  def valor(self) -> float:
    return self._valor

  @valor.setter
  def valor(self, value: float) -> None:
    if value < 0:
      raise ValueError("El precio no puede ser negativo.")
    self._valor = float(value)

  @property
  def moneda(self) -> Moneda:
    return self._moneda

  @moneda.setter
  def moneda(self, value: Moneda) -> None:
    if not isinstance(value, Moneda):
      raise TypeError("La moneda debe ser una instancia de Moneda.")
    self._moneda = value

  @property
  def fecha(self) -> datetime.date:
    return self._fecha

  @fecha.setter
  def fecha(self, value: datetime.date) -> None:
    if not isinstance(value, datetime.date):
      raise TypeError("La fecha debe ser una instancia de datetime.date.")
    self._fecha = value


class Producto(EntidadBase):
  """Producto comercializado por el negocio."""

  def __init__(
      self,
      id: int,
      nombre: str,
      descripcion: str,
      precio: Precio,
      categoria: Categoria,
      proveedor: Proveedor,
  ) -> None:
    super().__init__(id)
    self.nombre = nombre
    self.descripcion = descripcion
    self.precio = precio
    self.categoria = categoria
    self.proveedor = proveedor

  @property
  def nombre(self) -> str:
    return self._nombre

  @nombre.setter
  def nombre(self, value: str) -> None:
    if not value or not value.strip():
      raise ValueError("El nombre del producto es obligatorio.")
    self._nombre = value.strip()

  @property
  def descripcion(self) -> str:
    return self._descripcion

  @descripcion.setter
  def descripcion(self, value: str) -> None:
    self._descripcion = value.strip() if value else ""

  @property
  def precio(self) -> Precio:
    return self._precio

  @precio.setter
  def precio(self, value: Precio) -> None:
    if not isinstance(value, Precio):
      raise TypeError("El precio debe ser una instancia de Precio.")
    self._precio = value

  @property
  def categoria(self) -> Categoria:
    return self._categoria

  @categoria.setter
  def categoria(self, value: Categoria) -> None:
    if not isinstance(value, Categoria):
      raise TypeError("La categoria debe ser una instancia de Categoria.")
    self._categoria = value

  @property
  def proveedor(self) -> Proveedor:
    return self._proveedor

  @proveedor.setter
  def proveedor(self, value: Proveedor) -> None:
    if not isinstance(value, Proveedor):
      raise TypeError("El proveedor debe ser una instancia de Proveedor.")
    self._proveedor = value


class Stock:
  """Cantidad disponible de un producto en un almacen."""

  def __init__(
      self,
      producto: Producto,
      cantidad: int,
      almacen: str = "Principal",
  ) -> None:
    self.producto = producto
    self.cantidad = cantidad
    self.almacen = almacen

  @property
  def producto(self) -> Producto:
    return self._producto

  @producto.setter
  def producto(self, value: Producto) -> None:
    if not isinstance(value, Producto):
      raise TypeError("El stock debe estar asociado a un Producto.")
    self._producto = value

  @property
  def producto_id(self) -> int:
    return self.producto.id

  @property
  def cantidad(self) -> int:
    return self._cantidad

  @cantidad.setter
  def cantidad(self, value: int) -> None:
    if not isinstance(value, int) or value < 0:
      raise ValueError("La cantidad de stock no puede ser negativa.")
    self._cantidad = value

  @property
  def almacen(self) -> str:
    return self._almacen

  @almacen.setter
  def almacen(self, value: str) -> None:
    if not value or not value.strip():
      raise ValueError("El almacen es obligatorio.")
    self._almacen = value.strip()


class CotizacionDolar:
  """Cotizacion del dolar para una fecha y tipo determinado."""

  def __init__(
      self,
      valor: float,
      fecha: datetime.date,
      tipo: TipoCotizacion,
  ) -> None:
    self.valor = valor
    self.fecha = fecha
    self.tipo = tipo

  @property
  def valor(self) -> float:
    return self._valor

  @valor.setter
  def valor(self, value: float) -> None:
    if value <= 0:
      raise ValueError("La cotizacion debe ser positiva.")
    self._valor = float(value)

  @property
  def fecha(self) -> datetime.date:
    return self._fecha

  @fecha.setter
  def fecha(self, value: datetime.date) -> None:
    if not isinstance(value, datetime.date):
      raise TypeError("La fecha debe ser una instancia de datetime.date.")
    self._fecha = value

  @property
  def tipo(self) -> TipoCotizacion:
    return self._tipo

  @tipo.setter
  def tipo(self, value: TipoCotizacion) -> None:
    if not isinstance(value, TipoCotizacion):
      raise TypeError("El tipo debe ser una instancia de TipoCotizacion.")
    self._tipo = value
