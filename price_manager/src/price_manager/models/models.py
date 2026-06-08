from datetime import datetime, timezone, timedelta
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import relationship
from price_manager.database.connection import Base

# MODELO DE CATEGORÍAS
class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

# MODELO DE PROVEEDORES
class Proveedor(Base):
    __tablename__ = 'proveedores'
    id = Column(Integer, primary_key=True, index=True)
    nombre_legal = Column(String, unique=True, index=True)
    contacto = Column(String)

# MODELO DE PRECIOS
class Precio(Base):
    __tablename__ = 'precios'
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float)
    moneda = Column(String)
    ultima_actualizacion = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-3))).replace(tzinfo=None))

# MODELO DE PRODUCTOS
class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    proveedor_id = Column(Integer, ForeignKey('proveedores.id'))
    precio_id = Column(Integer, ForeignKey('precios.id'))

    categoria = relationship("Categoria")
    proveedor = relationship("Proveedor")
    precio = relationship("Precio")

# MODELO DE COTIZACIONES DEL DÓLAR
class CotizacionDolar(Base):
    __tablename__ = 'cotizaciones_dolar'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    compra = Column(Float)
    venta = Column(Float)
    fecha_actualizacion = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-3))).replace(tzinfo=None))

# MODELO DE AUDITORÍA (SPRINT 3)
class Auditoria(Base):
    __tablename__ = 'auditoria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    accion = Column(String, nullable=False)
    fecha = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-3))).replace(tzinfo=None))
    detalle = Column(String)

# MODELO DE PRECIOS COMPETENCIA (SPRINT 3)
class PrecioCompetencia(Base):
    __tablename__ = 'precios_competencia'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_interno_id = Column(Integer, ForeignKey('productos.id'))
    nombre_web = Column(String, nullable=False)
    precio_web = Column(Float, nullable=False)
    imagen_url = Column(String)
    descripcion_web = Column(String)
    formas_pago = Column(String)  # Se guardará como representación JSON o texto estructurado
    fecha_extraccion = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-3))).replace(tzinfo=None))

    producto = relationship("Producto")