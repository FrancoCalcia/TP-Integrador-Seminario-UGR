import csv
import datetime
import os
from typing import Dict

from price_manager.entities.entities import (
    Categoria,
    CotizacionDolar,
    Moneda,
    Precio,
    Producto,
    Proveedor,
    Stock,
    TipoCotizacion,
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


def _ruta_csv(nombre_archivo: str) -> str:
    """Construye la ruta absoluta al archivo CSV de migracion."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "migrations", "csv", nombre_archivo)


def _leer_csv(nombre_archivo: str) -> list:
    """Lee un CSV y devuelve una lista de diccionarios."""
    ruta = _ruta_csv(nombre_archivo)
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)


def cargar_categorias(
    servicio: ServicioCategoria,
) -> Dict[int, Categoria]:
    """Carga categorias desde el CSV y devuelve un mapa id->entidad."""
    mapa: Dict[int, Categoria] = {}
    for fila in _leer_csv("categoria.csv"):
        cat = Categoria(
            id=int(fila["id"]),
            nombre=fila["nombre"],
        )
        servicio.crear(cat)
        mapa[cat.id] = cat
    return mapa


def cargar_proveedores(
    servicio: ServicioProveedor,
) -> Dict[int, Proveedor]:
    """Carga proveedores desde el CSV y devuelve un mapa id->entidad."""
    mapa: Dict[int, Proveedor] = {}
    for fila in _leer_csv("proveedor.csv"):
        prov = Proveedor(
            id=int(fila["id"]),
            nombre=fila["nombre"],
            contacto=fila["contacto"],
        )
        servicio.crear(prov)
        mapa[prov.id] = prov
    return mapa


def cargar_monedas(
    servicio: ServicioMoneda,
) -> Dict[int, Moneda]:
    """Carga monedas desde el CSV y devuelve un mapa id->entidad."""
    mapa: Dict[int, Moneda] = {}
    for fila in _leer_csv("moneda.csv"):
        mon = Moneda(
            id=int(fila["id"]),
            nombre=fila["nombre"],
            codigo=fila["codigo"],
        )
        servicio.crear(mon)
        mapa[mon.id] = mon
    return mapa


def cargar_tipos_cotizacion(
    servicio: ServicioTipoCotizacion,
) -> Dict[int, TipoCotizacion]:
    """Carga tipos de cotizacion desde el CSV y devuelve un mapa."""
    mapa: Dict[int, TipoCotizacion] = {}
    for fila in _leer_csv("tipo_cotizacion.csv"):
        tipo = TipoCotizacion(
            id=int(fila["id"]),
            nombre=fila["nombre"],
        )
        servicio.crear(tipo)
        mapa[tipo.id] = tipo
    return mapa


def cargar_productos(
    servicio: ServicioProducto,
    monedas: Dict[int, Moneda],
    categorias: Dict[int, Categoria],
    proveedores: Dict[int, Proveedor],
) -> Dict[int, Producto]:
    """Carga productos desde el CSV y devuelve un mapa id->entidad."""
    mapa: Dict[int, Producto] = {}
    for fila in _leer_csv("producto.csv"):
        precio = Precio(
            valor=float(fila["precio_valor"]),
            moneda=monedas[int(fila["precio_moneda_id"])],
            fecha=datetime.date.fromisoformat(fila["precio_fecha"]),
        )
        prod = Producto(
            id=int(fila["id"]),
            nombre=fila["nombre"],
            descripcion=fila["descripcion"],
            precio=precio,
            categoria=categorias[int(fila["categoria_id"])],
            proveedor=proveedores[int(fila["proveedor_id"])],
        )
        servicio.crear(prod)
        mapa[prod.id] = prod
    return mapa


def cargar_stock(
    servicio: ServicioStock,
    productos: Dict[int, Producto],
) -> None:
    """Carga stock desde el CSV."""
    for fila in _leer_csv("stock.csv"):
        producto_id = int(fila["producto_id"])
        cantidad = int(fila["cantidad"])
        servicio.registrar_movimiento(producto_id, cantidad)


def cargar_cotizaciones(
    servicio: ServicioCotizacionDolar,
    tipos: Dict[int, TipoCotizacion],
) -> None:
    """Carga cotizaciones del dolar desde el CSV."""
    for fila in _leer_csv("cotizacion_dolar.csv"):
        cotizacion = CotizacionDolar(
            valor=float(fila["valor"]),
            fecha=datetime.date.fromisoformat(fila["fecha"]),
            tipo=tipos[int(fila["tipo_id"])],
        )
        servicio.registrar_cotizacion(cotizacion)


def cargar_todos_los_datos(
    srv_cat: ServicioCategoria,
    srv_prov: ServicioProveedor,
    srv_mon: ServicioMoneda,
    srv_tipo_cot: ServicioTipoCotizacion,
    srv_prod: ServicioProducto,
    srv_stock: ServicioStock,
    srv_cot: ServicioCotizacionDolar,
) -> None:
    """Carga todos los datos desde los CSV en el orden correcto."""
    categorias = cargar_categorias(srv_cat)
    proveedores = cargar_proveedores(srv_prov)
    monedas = cargar_monedas(srv_mon)
    tipos = cargar_tipos_cotizacion(srv_tipo_cot)
    productos = cargar_productos(
        srv_prod,
        monedas,
        categorias,
        proveedores,
    )
    cargar_stock(srv_stock, productos)
    cargar_cotizaciones(srv_cot, tipos)
    print("Datos precargados desde CSV exitosamente.")
