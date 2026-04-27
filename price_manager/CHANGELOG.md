# CHANGELOG

Registro de cambios reconstruido para el Sprint 1. Cada dia representa un
punto o ejercicio distinto del trabajo practico.

## Sprint 1 - Price Manager

### Dia 1 - Inicializacion del proyecto

- Se creo la estructura base del proyecto `price_manager`.
- Se definio la rama de trabajo `Sprint_1`.
- Se organizaron las carpetas principales para entidades, repositorios,
  servicios, datos iniciales, migraciones CSV e interfaz de consola.
- Se agregaron archivos base del proyecto, incluyendo `README.md`,
  `requirements.txt` y punto de entrada inicial.

### Dia 2 - Modelado de entidades

- Se implemento la entidad base con identificador numerico positivo.
- Se agregaron las entidades de dominio: categoria, proveedor, moneda, tipo de
  cotizacion, precio, producto, stock y cotizacion del dolar.
- Se incorporaron validaciones de datos obligatorios, valores positivos,
  codigos de moneda y fechas.
- Se centralizo la logica comun de validacion dentro de las clases del dominio.

### Dia 3 - Repositorios en memoria

- Se definieron interfaces para repositorios CRUD.
- Se implementaron repositorios en memoria para categorias, proveedores,
  monedas, productos y tipos de cotizacion.
- Se agregaron repositorios especificos para stock y cotizaciones del dolar.
- Se contemplaron busquedas por id, por producto, por tipo de cotizacion y por
  fecha segun correspondiera.

### Dia 4 - Servicios de aplicacion

- Se crearon servicios para separar la logica de uso respecto de los
  repositorios.
- Se agregaron servicios para categorias, proveedores, monedas, productos,
  stock, tipos de cotizacion y cotizaciones.
- Se incorporaron validaciones de existencia antes de consultar, actualizar o
  eliminar registros.
- Se preparo la capa de servicios para ser consumida desde la interfaz de
  consola.

### Dia 5 - Precarga y datos CSV

- Se agregaron archivos CSV dentro de `migrations/csv`.
- Se cargaron datos iniciales de categorias, proveedores, monedas, productos,
  stock, tipos de cotizacion y cotizaciones del dolar.
- Se implemento el modulo de precarga para leer los CSV y crear las entidades
  correspondientes.
- Se verifico que la aplicacion pueda iniciar con datos disponibles para las
  pruebas del sprint.

### Dia 6 - Aplicacion de consola

- Se implemento el menu principal de la aplicacion.
- Se agregaron opciones para listar, crear, actualizar y eliminar categorias.
- Se agregaron opciones para listar productos, crear productos y actualizar
  precios.
- Se incorporaron consultas y movimientos de stock.
- Se agregaron operaciones para listar, registrar, actualizar y eliminar
  cotizaciones del dolar.

### Dia 7 - Validaciones, persistencia y pruebas

- Se agregaron validaciones de entrada para numeros enteros, importes, fechas y
  textos obligatorios.
- Se implemento persistencia en CSV para cambios realizados desde la consola en
  categorias, productos, stock y cotizaciones.
- Se ajusto el archivo `main.py` para construir repositorios, servicios,
  precargar datos y ejecutar la consola.
- Se probo el flujo principal con el test provisto por la catedra y con pruebas
  manuales desde la consola.

### Dia 8 - Documentacion y cierre del sprint

- Se completo el `README.md` con objetivo, contexto, estructura del proyecto,
  requisitos y forma de ejecucion.
- Se reviso la estructura final del Sprint 1.
- Se corrigieron detalles de mensajes, nombres y organizacion de archivos.
- Se dejo constancia de los cambios principales en este `CHANGELOG.md`.
