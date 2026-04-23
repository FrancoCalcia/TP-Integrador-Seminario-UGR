import sys
from pathlib import Path

# GC: Esto acá lo pongo para poder ejecutar desde la raíz del proyecto sin problemas de importación :P
SRC_PATH = Path(__file__).resolve().parents[1]
if str(SRC_PATH) not in sys.path:
  sys.path.insert(0, str(SRC_PATH))
  
import datetime

from price_manager.entities.entities import (
    Categoria, Proveedor, Moneda, TipoCotizacion, Precio, Producto, CotizacionDolar,
)
from price_manager.repositories.repositories import (
    RepositorioCategoria, RepositorioProveedor, RepositorioMoneda,
    RepositorioTipoCotizacion, RepositorioProducto, RepositorioStock,
    RepositorioCotizacionDolar,
)
from price_manager.services.services import (
    ServicioCategoria, ServicioProveedor, ServicioMoneda,
    ServicioTipoCotizacion, ServicioProducto, ServicioStock,
    ServicioCotizacionDolar,
)

print("🚀 Iniciando Batería de Pruebas de Integración (COBERTURA TOTAL)...\n")

# ==========================================
# 1. SETUP COMPLETO
# ==========================================
print("⚙️  Configurando entorno completo...")
repo_cat = RepositorioCategoria()
repo_prov = RepositorioProveedor()
repo_mon = RepositorioMoneda()
repo_prod = RepositorioProducto()
repo_stock = RepositorioStock()
repo_tipo_cot = RepositorioTipoCotizacion()
repo_cot = RepositorioCotizacionDolar()

srv_cat = ServicioCategoria(repo_cat)
srv_prov = ServicioProveedor(repo_prov)
srv_mon = ServicioMoneda(repo_mon)
srv_prod = ServicioProducto(repo_prod, srv_cat, srv_prov)
srv_stock = ServicioStock(repo_stock, srv_prod)
srv_tipo_cot = ServicioTipoCotizacion(repo_tipo_cot)
srv_cot = ServicioCotizacionDolar(repo_cot, srv_tipo_cot)

# ==========================================
# 2. PRUEBAS DE CREACIÓN Y LECTURA BASE
# ==========================================
print("\n🧪 Prueba 1: Creación de Entidades Maestras...")
cat1 = Categoria(id=1, nombre="Electrónica")
prov1 = Proveedor(id=1, nombre="TechCorp", contacto="ventas@tech.com")
mon1 = Moneda(id=1, nombre="Peso Argentino")

srv_cat.crear(cat1)
srv_prov.crear(prov1)
srv_mon.crear(mon1)

assert len(srv_cat.listar_todos()) == 1, "Fallo: No se guardó la categoría"
print("✅ Prueba 1 Superada: Lectura y Creación de maestras ok.")

# ==========================================
# 3. PRUEBAS DE PRODUCTO (CREAR Y LEER)
# ==========================================
print("\n🧪 Prueba 2: Creación de Producto...")
precio1 = Precio(valor=150000.0, moneda=mon1, fecha=datetime.date.today())
prod1 = Producto(
    id=100, nombre="Monitor 24", descripcion="Full HD",
    precio=precio1, categoria=cat1, proveedor=prov1
)

srv_prod.crear(prod1)
assert srv_prod.obtener(100).nombre == "Monitor 24", "Fallo: No se pudo leer el producto."
print("✅ Prueba 2 Superada: Producto creado y leído correctamente.")

# ==========================================
# 4. PRUEBAS DE ACTUALIZACIÓN (UPDATE)
# ==========================================
print("\n🧪 Prueba 3: Actualización de Entidades...")

# Modificamos el producto
prod_a_modificar = srv_prod.obtener(100)
prod_a_modificar.nombre = "Monitor 24 Pro Max"
prod_a_modificar.precio.valor = 180000.0

srv_prod.actualizar(prod_a_modificar)

prod_actualizado = srv_prod.obtener(100)
assert prod_actualizado.nombre == "Monitor 24 Pro Max", "Fallo: No se actualizó el nombre"
assert prod_actualizado.precio.valor == 180000.0, "Fallo: No se actualizó el precio"

try:
    prod_fantasma = Producto(id=999, nombre="Nada", descripcion="", precio=precio1, categoria=cat1, proveedor=prov1)
    srv_prod.actualizar(prod_fantasma)
    assert False, "Fallo crítico: Permitió actualizar un producto inexistente."
except ValueError as e:
    print(f"  ✔️  Error esperado capturado: {e}")

print("✅ Prueba 3 Superada: Método 'actualizar' funciona a la perfección.")

# ==========================================
# 5. PRUEBAS DE ELIMINACIÓN (DELETE)
# ==========================================
print("\n🧪 Prueba 4: Eliminación de Entidades...")

prod_temporal = Producto(
    id=200, nombre="Mouse", descripcion="Óptico",
    precio=precio1, categoria=cat1, proveedor=prov1
)
srv_prod.crear(prod_temporal)
assert len(srv_prod.listar_todos()) == 2, "Debería haber 2 productos."

srv_prod.eliminar(200)
assert len(srv_prod.listar_todos()) == 1, "Debería quedar solo 1 producto tras borrar."

try:
    srv_prod.obtener(200)
    assert False, "Fallo crítico: El producto sigue existiendo tras eliminarlo."
except ValueError:
    pass

try:
    srv_prod.eliminar(999)
    assert False, "Fallo crítico: Permitió eliminar un ID inexistente sin avisar."
except ValueError as e:
    print(f"  ✔️  Error esperado capturado: {e}")

print("✅ Prueba 4 Superada: Método 'eliminar' blindado.")

# ==========================================
# 6. PRUEBAS DE FLUJO DE STOCK (MATEMÁTICA)
# ==========================================
print("\n🧪 Prueba 5: Lógica Matemática de Stock...")
srv_stock.registrar_movimiento(100, 50)
srv_stock.registrar_movimiento(100, -20)
assert srv_stock.obtener_stock(100) == 30, "Fallo: El stock debería ser 30"

try:
    srv_stock.registrar_movimiento(100, -40)
    assert False, "Fallo crítico: Permitió stock negativo."
except ValueError as e:
    print(f"  ✔️  Error esperado capturado: {e}")
print("✅ Prueba 5 Superada: Inventario y validaciones matemáticas correctas.")

# ==========================================
# 7. PRUEBAS DE COTIZACIONES (HISTÓRICOS)
# ==========================================
print("\n🧪 Prueba 6: Histórico de Cotizaciones...")

tipo_blue = TipoCotizacion(id=1, nombre="Dólar Blue")
srv_tipo_cot.crear(tipo_blue)

cot_1 = CotizacionDolar(valor=980.0, fecha=datetime.date(2023, 10, 1), tipo=tipo_blue)
cot_2 = CotizacionDolar(valor=1000.0, fecha=datetime.date(2023, 10, 2), tipo=tipo_blue)
cot_3 = CotizacionDolar(valor=950.0, fecha=datetime.date(2023, 10, 3), tipo=tipo_blue)

srv_cot.registrar_cotizacion(cot_1)
srv_cot.registrar_cotizacion(cot_2)
srv_cot.registrar_cotizacion(cot_3)

historico = srv_cot.obtener_historico(1)
assert len(historico) == 3, "Fallo: Deberían haberse recuperado 3 cotizaciones históricas."
assert historico[1].valor == 1000.0, "Fallo: El orden o el valor de la cotización es incorrecto."

try:
    srv_cot.obtener_historico(99)
    assert False, "Fallo crítico: Permitió consultar histórico de un tipo inexistente."
except ValueError as e:
    print(f"  ✔️  Error esperado capturado: {e}")

print("✅ Prueba 6 Superada: Circuito de cotizaciones y registro histórico validado.")

print("\n🎉 ¡TODAS LAS PRUEBAS (CRUD COMPLETO Y NEGOCIO) PASARON CON ÉXITO! 🎉")
