# CHANGELOG - Price Manager Grupo 14

## Sprint 3

### [Ejercicio 07] - Menú CLI de Price Manager
- Se agregaron nuevas opciones al menú interactivo de consola en `price_manager/ui/console.py` para soportar las operaciones del Sprint 3.
- Se implementaron las opciones:
  - `4. Ejecutar scraping (Competencia)`: Lanza la extracción automatizada sobre la competencia.
  - `5. Generar reporte comparativo e ingresar alertas`: Crea el Excel de comparación y solicita un umbral en pesos para generar alertas CSV.
  - `6. Ver historial de auditoría`: Muestra de forma tabular la base de auditorías registradas.

### [Ejercicio 06] - Auditorías y Decorador de Registro
- Se creó el decorador `@auditar` en `price_manager/utils/audit.py` que registra automáticamente el éxito o fallo de las acciones críticas.
- Se definió el modelo `Auditoria` en `price_manager/models/models.py` para almacenar `accion`, `fecha` y `detalle`.
- Se decoraron los métodos principales de interacción en el controlador del menú CLI.

### [Ejercicio 05] - Reporte Comparativo en Excel
- Se implementó la generación de reportes en formato Excel (`.xlsx`) en `price_manager/services/report_service.py` utilizando `pandas` y `openpyxl`.
- El reporte consolida para cada producto: Nombre, Precio Interno, Precio Competencia, Diferencia de Precios y la Fecha de Extracción.
- Los reportes se guardan con timestamp en un directorio exclusivo para descargas.

### [Ejercicio 04] - Generación de Alertas de Precios (CSV)
- Se desarrolló el servicio de comparación en `price_manager/services/report_service.py` que recibe una diferencia máxima permitida (threshold).
- Se genera un archivo CSV con las alertas de desviaciones críticas que exceden el límite definido por el usuario para cada producto.

### [Ejercicio 03] - Scraper Scrapy (Star Computación)
- Se creó la estructura del scraper Scrapy bajo `price_manager/scraper/`.
- Se implementó `StarComputacionSpider` para buscar automáticamente los productos de nuestro inventario y extraer el precio de venta al contado/débito, descripción extendida, formas de pago y la URL de la imagen del producto.
- Se diseñó la canalización utilizando `ItemLoader` y `PrecioCompetenciaPipeline` para formatear los precios e insertar los resultados extraídos directamente en la tabla `precios_competencia`.
- Se configuró la ejecución sobre subprocesos en Windows para asegurar la compatibilidad con el loop de eventos de Twisted.

---

## Sprint 2

### [Ejercicio 02] - Migraciones de Datos Históricos
- Se implementó la utilidad `cargar_sqls` para ejecutar archivos de migración estructurados.
- Se crearon los scripts SQL en `migrations/sql/` para precargar y poblar las tablas base de categorías, proveedores, precios y productos desde los CSV históricos.

### [Ejercicio 01] - Arquitectura Modular y Persistencia ORM
- Se migró el almacenamiento del inventario a una base de datos relacional SQLite utilizando SQLAlchemy.
- Se implementaron las entidades y modelos relacionales del dominio (`Categoria`, `Proveedor`, `Precio`, `Producto`, `CotizacionDolar`) en `price_manager/models/models.py`.
- Se configuró el context manager de transacciones `session_scope` en `price_manager/database/connection.py`.
