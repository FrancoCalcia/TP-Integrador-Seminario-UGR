# Changelog

## Sprint 1

### Día 1 — Inicialización del proyecto y versionado

- Se creó el repositorio en GitHub y se configuró el acceso por token.
- Se definió la rama de trabajo `Sprint_1`.
- Se generó la estructura de directorios del proyecto.
- Se crearon los archivos base: `README.md`, `CHANGELOG.md` y
  `requirements.txt`.
- Se definió la variable `desactivar_git_push` para controlar los push.

### Día 2 — Clases entidad

- Se implementaron las clases de dominio aplicando encapsulamiento y POO:
  `EntidadBase`, `Categoria`, `Proveedor`, `Moneda`, `TipoCotizacion`,
  `Precio`, `Producto`, `Stock` y `CotizacionDolar`.
- Se incorporaron validaciones de datos en cada propiedad.
- Se aplicaron Type Hints e indentación de 2 espacios (PEP8).

### Día 3 — Repositorios y CRUD

- Se definieron las interfaces abstractas para repositorios.
- Se implementó el repositorio genérico en memoria.
- Se crearon repositorios concretos para cada entidad con CRUD completo.

### Día 4 — Servicios de lógica de negocio

- Se crearon los servicios para cada entidad del dominio.
- Se incorporaron validaciones de existencia antes de operar sobre registros.
- Se implementó la lógica de movimiento de stock y registro de cotizaciones.

### Día 5 — Precarga de datos desde archivos CSV

- Se crearon los archivos CSV en `migrations/csv/` con al menos 10 registros
  por entidad: categorías, proveedores, monedas, tipos de cotización,
  productos, stock y cotizaciones del dólar.
- Se implementó el módulo `preload_data.py` con la función
  `cargar_todos_los_datos`.

### Día 6 — Interfaz de consola

- Se implementó `ui/console.py` con la clase `ConsoleUI`.
- Se creó el menú interactivo con operaciones CRUD para cada entidad.

### Día 7 — Punto de entrada y cierre del sprint

- Se creó `main.py` como punto de entrada de la aplicación.
- Se configuró la precarga automática de datos al iniciar.
- Se completó el `README.md` con el objetivo y el contexto del sprint.

---

## Sprint 2

### Día 1 — Inicialización del repositorio y nueva estructura

- Se clonó el repositorio usando `GITHUB_TOKEN` (secret de Colab).
- Se creó la rama `Sprint_2` a partir de `Sprint_1`.
- Se extendió la estructura de directorios incorporando `database/`,
  `models/` y `migrations/sql/`.

### Día 2 — Clase ConexionDB

- Se creó `database/connection.py` con la clase `ConexionDB`.
- Se gestionó la conexión a SQLite con `create_engine` y `sessionmaker`.
- Se expuso la instancia global `db_manager`.

### Día 3 — Context manager de transacciones

- Se agregó `session_scope()` como context manager en `connection.py`.
- Se implementó el manejo seguro de `commit`, `rollback` y `close`.

### Día 4 — Modelos ORM y tablas

- Se crearon los modelos en `models/models.py`: `Categoria`, `Proveedor`,
  `Precio`, `Producto` y `CotizacionDolar`.
- Se definieron columnas, claves foráneas y relaciones entre tablas.
- Se ejecutó `Base.metadata.create_all()` para crear las tablas en SQLite.

### Día 5 — Migración de datos CSV a la base de datos

- Se creó `migrations/migrations.py` con la función `migrar_datos()`.
- Se migraron los datos de los CSV del Sprint 1 a la base de datos.
- Se generaron archivos `.sql` con las sentencias de inserción en
  `migrations/sql/`.

### Día 6 — Repositorios con base de datos

- Se actualizó `repositories/repositories.py` para operar sobre SQLAlchemy.
- Se implementaron `ProductoRepository`, `CategoriaRepository` y
  `ProveedorRepository` con métodos `get_all`, `get_by_id` y `add`.

### Día 7 — API del dólar y dotenv

- Se creó el archivo `.env` con `API_URL=https://dolarapi.com/v1/dolares`.
- Se actualizó `services/services.py` con la clase `ServicioCotizacionDolar`.
- Se implementó `obtener_cotizaciones()` para consultar la API y persistir
  los resultados en la base de datos.

### Día 8 — Extensión del menú de consola

- Se actualizó `ui/console.py` con tres nuevas opciones: obtener
  cotizaciones por API, ver lista de precios bimonetaria y exportar
  precios a CSV.
- Se actualizó `main.py` como punto de entrada del sistema.
- Se completó el `README.md` con la introducción y el contexto del Sprint 2.
