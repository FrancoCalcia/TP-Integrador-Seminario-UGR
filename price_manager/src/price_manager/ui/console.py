import datetime
import csv
import os
from pathlib import Path

from price_manager.entities.entities import (
  Categoria,
  CotizacionDolar,
  Precio,
  Producto,
)


class ConsoleApp:
  """Interfaz de consola simple con un bucle principal."""

  def __init__(
      self,
      srv_categoria,
      srv_proveedor,
      srv_moneda,
      srv_tipo_cotizacion,
      srv_producto,
      srv_stock,
      srv_cotizacion,
  ) -> None:
    self.srv_categoria = srv_categoria
    self.srv_proveedor = srv_proveedor
    self.srv_moneda = srv_moneda
    self.srv_tipo_cotizacion = srv_tipo_cotizacion
    self.srv_producto = srv_producto
    self.srv_stock = srv_stock
    self.srv_cotizacion = srv_cotizacion

  def run(self) -> None:
    """Ejecuta el menú principal en loop hasta que el usuario salga."""
    while True:
      self._mostrar_menu()
      opcion = input("Seleccione una opcion: ").strip()

      if opcion.lower() in {"c", "clear"}:
        self._limpiar_pantalla()
        continue

      if opcion == "0":
        print("Saliendo del sistema.")
        break

      try:
        self._ejecutar_opcion(opcion)
      except Exception as error:
        print(f"Error: {error}")

  def _mostrar_menu(self) -> None:
    print("\n=== PRICE MANAGER ===")
    print("1) Listar categorias")
    print("2) Crear categoria")
    print("3) Actualizar categoria")
    print("4) Eliminar categoria")
    print("5) Listar productos")
    print("6) Crear producto")
    print("7) Actualizar producto")
    print("8) Eliminar producto")
    print("9) Consultar stock de producto")
    print("10) Registrar movimiento de stock")
    print("11) Listar cotizaciones")
    print("12) Registrar cotizacion")
    print("13) Actualizar cotizacion")
    print("14) Eliminar cotizacion")
    print("C) Limpiar pantalla")
    print("0) Salir")

  def _ejecutar_opcion(self, opcion: str) -> None:
    acciones = {
      "1": self._listar_categorias,
      "2": self._crear_categoria,
      "3": self._actualizar_categoria,
      "4": self._eliminar_categoria,
      "5": self._listar_productos,
      "6": self._crear_producto,
      "7": self._actualizar_precio_producto,
      "8": self._eliminar_producto,
      "9": self._consultar_stock,
      "10": self._registrar_movimiento_stock,
      "11": self._listar_cotizaciones,
      "12": self._registrar_cotizacion,
      "13": self._actualizar_cotizacion,
      "14": self._eliminar_cotizacion,
    }
    accion = acciones.get(opcion)
    if not accion:
      print("Opcion invalida.")
      return
    accion()

  def _listar_categorias(self) -> None:
    categorias = self.srv_categoria.listar_todos()
    if not categorias:
      print("No hay categorias cargadas.")
      return
    for categoria in categorias:
      print(f"[{categoria.id}] {categoria.nombre}")

  def _crear_categoria(self) -> None:
    id_categoria = self._pedir_int("ID categoria: ")
    nombre = self._pedir_texto("Nombre categoria: ")
    categoria = Categoria(id=id_categoria, nombre=nombre)
    self.srv_categoria.crear(categoria)
    self._persistir_categorias_csv()
    print("Categoria creada.")

  def _actualizar_categoria(self) -> None:
    id_categoria = self._pedir_int("ID categoria a actualizar: ")
    categoria = self.srv_categoria.obtener(id_categoria)
    nombre = self._pedir_texto(
      f"Nuevo nombre ({categoria.nombre}): ",
      permitir_vacio=True,
    )
    if nombre:
      categoria.nombre = nombre
      self.srv_categoria.actualizar(categoria)
      self._persistir_categorias_csv()
    print("Categoria actualizada.")

  def _eliminar_categoria(self) -> None:
    id_categoria = self._pedir_int("ID categoria a eliminar: ")
    self.srv_categoria.eliminar(id_categoria)
    self._persistir_categorias_csv()
    print("Categoria eliminada.")

  def _persistir_categorias_csv(self) -> None:
    """Guarda el estado actual de categorias en migrations/csv/categoria.csv."""
    ruta = Path(__file__).resolve().parents[1] / "migrations" / "csv" / "categoria.csv"
    categorias = sorted(self.srv_categoria.listar_todos(), key=lambda categoria: categoria.id)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
      writer = csv.writer(archivo)
      writer.writerow(["id", "nombre"])
      for categoria in categorias:
        writer.writerow([categoria.id, categoria.nombre])

  def _listar_productos(self) -> None:
    productos = self.srv_producto.listar_todos()
    if not productos:
      print("No hay productos cargados.")
      return
    for producto in productos:
      print(
        f"[{producto.id}] {producto.nombre} | "
        f"{producto.precio.valor:.2f} {producto.precio.moneda.codigo} | "
        f"categoria={producto.categoria.nombre} | "
        f"proveedor={producto.proveedor.nombre}"
      )

  def _crear_producto(self) -> None:
    id_producto = self._pedir_int("ID producto: ")
    nombre = self._pedir_texto("Nombre: ")
    descripcion = self._pedir_texto("Descripcion: ", permitir_vacio=True)
    valor = self._pedir_float("Precio valor: ")
    fecha = self._pedir_fecha("Fecha precio (YYYY-MM-DD): ")

    self._mostrar_monedas_disponibles()
    id_moneda = self._pedir_int("ID moneda: ")

    self._mostrar_categorias_disponibles()
    id_categoria = self._pedir_int("ID categoria: ")

    self._mostrar_proveedores_disponibles()
    id_proveedor = self._pedir_int("ID proveedor: ")

    moneda = self.srv_moneda.obtener(id_moneda)
    categoria = self.srv_categoria.obtener(id_categoria)
    proveedor = self.srv_proveedor.obtener(id_proveedor)
    precio = Precio(valor=valor, moneda=moneda, fecha=fecha)

    producto = Producto(
      id=id_producto,
      nombre=nombre,
      descripcion=descripcion,
      precio=precio,
      categoria=categoria,
      proveedor=proveedor,
    )
    self.srv_producto.crear(producto)
    self._persistir_productos_csv()
    print("Producto creado.")

  def _actualizar_precio_producto(self) -> None:
    id_producto = self._pedir_int("ID producto: ")
    producto = self.srv_producto.obtener(id_producto)
    nuevo_nombre = self._pedir_texto(
      f"Nuevo nombre ({producto.nombre}): ",
      permitir_vacio=True,
    )
    nueva_descripcion = self._pedir_texto(
      f"Nueva descripcion ({producto.descripcion}): ",
      permitir_vacio=True,
    )
    nuevo_valor = self._pedir_float("Nuevo precio valor: ")
    nueva_fecha = self._pedir_fecha("Nueva fecha (YYYY-MM-DD): ")

    if nuevo_nombre:
      producto.nombre = nuevo_nombre
    if nueva_descripcion:
      producto.descripcion = nueva_descripcion
    producto.precio.valor = nuevo_valor
    producto.precio.fecha = nueva_fecha
    self.srv_producto.actualizar(producto)
    self._persistir_productos_csv()
    print("Producto actualizado.")

  def _eliminar_producto(self) -> None:
    id_producto = self._pedir_int("ID producto a eliminar: ")
    self.srv_producto.eliminar(id_producto)
    self._persistir_productos_csv()
    print("Producto eliminado.")

  def _consultar_stock(self) -> None:
    id_producto = self._pedir_int("ID producto: ")
    producto = self.srv_producto.obtener(id_producto)
    cantidad = self.srv_stock.obtener_stock(id_producto)
    print(f"Stock de {producto.nombre}: {cantidad}")

  def _registrar_movimiento_stock(self) -> None:
    id_producto = self._pedir_int("ID producto: ")
    cantidad = self._pedir_int(
      "Cantidad (positiva ingreso / negativa egreso): ",
      permitir_negativo=True,
    )
    self.srv_stock.registrar_movimiento(id_producto, cantidad)
    print("Movimiento registrado.")

  def _listar_cotizaciones(self) -> None:
    cotizaciones = self.srv_cotizacion.listar_todas()
    if not cotizaciones:
      print("No hay cotizaciones cargadas.")
      return
    for cotizacion in cotizaciones:
      print(
        f"tipo={cotizacion.tipo.nombre} "
        f"fecha={cotizacion.fecha.isoformat()} "
        f"valor={cotizacion.valor:.2f}"
      )

  def _registrar_cotizacion(self) -> None:
    self._mostrar_tipos_cotizacion_disponibles()
    id_tipo = self._pedir_int("ID tipo cotizacion: ")
    valor = self._pedir_float("Valor: ")
    fecha = self._pedir_fecha("Fecha (YYYY-MM-DD): ")
    tipo = self.srv_tipo_cotizacion.obtener(id_tipo)
    cotizacion = CotizacionDolar(valor=valor, fecha=fecha, tipo=tipo)
    self.srv_cotizacion.registrar_cotizacion(cotizacion)
    print("Cotizacion registrada.")

  def _actualizar_cotizacion(self) -> None:
    self._mostrar_tipos_cotizacion_disponibles()
    id_tipo = self._pedir_int("ID tipo cotizacion: ")
    fecha = self._pedir_fecha("Fecha existente (YYYY-MM-DD): ")
    cotizacion = self.srv_cotizacion.repo.leer_por_tipo_y_fecha(id_tipo, fecha)
    if not cotizacion:
      raise ValueError("Cotizacion no encontrada")
    nuevo_valor = self._pedir_float("Nuevo valor: ")
    cotizacion.valor = nuevo_valor
    self.srv_cotizacion.actualizar_cotizacion(cotizacion)
    print("Cotizacion actualizada.")

  def _eliminar_cotizacion(self) -> None:
    self._mostrar_tipos_cotizacion_disponibles()
    id_tipo = self._pedir_int("ID tipo cotizacion: ")
    fecha = self._pedir_fecha("Fecha a eliminar (YYYY-MM-DD): ")
    self.srv_cotizacion.eliminar_cotizacion(id_tipo, fecha)
    print("Cotizacion eliminada.")

  def _persistir_productos_csv(self) -> None:
    """Guarda el estado actual de productos en migrations/csv/producto.csv."""
    ruta = Path(__file__).resolve().parents[1] / "migrations" / "csv" / "producto.csv"
    productos = sorted(self.srv_producto.listar_todos(), key=lambda producto: producto.id)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
      writer = csv.writer(archivo)
      writer.writerow([
        "id",
        "nombre",
        "descripcion",
        "precio_valor",
        "precio_moneda_id",
        "precio_fecha",
        "categoria_id",
        "proveedor_id",
      ])
      for producto in productos:
        writer.writerow([
          producto.id,
          producto.nombre,
          producto.descripcion,
          producto.precio.valor,
          producto.precio.moneda.id,
          producto.precio.fecha.isoformat(),
          producto.categoria.id,
          producto.proveedor.id,
        ])

  def _mostrar_monedas_disponibles(self) -> None:
    print("Monedas disponibles:")
    for moneda in self.srv_moneda.listar_todos():
      print(f"  [{moneda.id}] {moneda.nombre} ({moneda.codigo})")

  def _mostrar_categorias_disponibles(self) -> None:
    print("Categorias disponibles:")
    for categoria in self.srv_categoria.listar_todos():
      print(f"  [{categoria.id}] {categoria.nombre}")

  def _mostrar_proveedores_disponibles(self) -> None:
    print("Proveedores disponibles:")
    for proveedor in self.srv_proveedor.listar_todos():
      print(f"  [{proveedor.id}] {proveedor.nombre}")

  def _mostrar_tipos_cotizacion_disponibles(self) -> None:
    print("Tipos de cotizacion disponibles:")
    for tipo in self.srv_tipo_cotizacion.listar_todos():
      print(f"  [{tipo.id}] {tipo.nombre}")

  def _limpiar_pantalla(self) -> None:
    if os.name == "nt":
      os.system("cls")
      return
    print("\n" * 60, end="")

  def _pedir_texto(self, mensaje: str, permitir_vacio: bool = False) -> str:
    while True:
      valor = input(mensaje).strip()
      if valor or permitir_vacio:
        return valor
      print("Entrada invalida. Ingrese un texto.")

  def _pedir_int(
      self,
      mensaje: str,
      permitir_negativo: bool = False,
  ) -> int:
    while True:
      valor = input(mensaje).strip()
      try:
        numero = int(valor)
      except ValueError:
        print("Entrada invalida. Ingrese un numero entero.")
        continue

      if not permitir_negativo and numero < 0:
        print("Entrada invalida. Debe ser un entero no negativo.")
        continue
      return numero

  def _pedir_float(self, mensaje: str) -> float:
    while True:
      valor = input(mensaje).strip().replace(",", ".")
      try:
        return float(valor)
      except ValueError:
        print("Entrada invalida. Ingrese un numero.")

  def _pedir_fecha(self, mensaje: str) -> datetime.date:
    while True:
      valor = input(mensaje).strip()
      try:
        return datetime.date.fromisoformat(valor)
      except ValueError:
        print("Fecha invalida. Use formato YYYY-MM-DD.")
