import csv
import os
from price_manager.database.connection import session_scope
from price_manager.models.models import Categoria, Proveedor, Precio, Producto

def migrar_datos(carpeta_csvs:str, carpeta_sqls:str):
    """Migra datos de todos los archivos CSV del Sprint 1 a la Base de Datos."""
    os.makedirs(carpeta_sqls, exist_ok=True)

    # MIGRACION DE PROVEEDORES
    _migrar_entidad(carpeta_csvs, carpeta_sqls, 'proveedores.csv', Proveedor,
                    lambda row: Proveedor(id=int(row['id']), nombre_legal=row['nombre_legal'], contacto=row['contacto']),
                    "INSERT INTO proveedores (id, nombre_legal, contacto) VALUES ({id}, '{nombre_legal}', '{contacto}');")

    # MIGRACION DE CATEGORIAS
    _migrar_entidad(carpeta_csvs, carpeta_sqls, 'categorias.csv', Categoria,
                    lambda row: Categoria(id=int(row['id']), nombre=row['nombre']),
                    "INSERT INTO categorias (id, nombre) VALUES ({id}, '{nombre}');")

    # MIGRACION DE PRECIOS
    _migrar_entidad(carpeta_csvs, carpeta_sqls, 'precios.csv', Precio,
                    lambda row: Precio(id=int(row['id']), valor=float(row['valor']), moneda=row['moneda']),
                    "INSERT INTO precios (id, valor, moneda) VALUES ({id}, {valor}, '{moneda}');")

    # MIGRACION DE PRODUCTOS
    _migrar_entidad(carpeta_csvs, carpeta_sqls, 'productos.csv', Producto,
                    lambda row: Producto(id=int(row['id']), nombre=row['nombre'], descripcion=row['descripcion'],
                                         categoria_id=int(row['categoria_id']), proveedor_id=int(row['proveedor_id']),
                                         precio_id=int(row['precio_id'])),
                    "INSERT INTO productos (id, nombre, descripcion, categoria_id, proveedor_id, precio_id) VALUES ({id}, '{nombre}', '{descripcion}', {categoria_id}, {proveedor_id}, {precio_id});")

    print("\n Migracion completa finalizada.")

def _migrar_entidad(carpeta_csv, carpeta_sql, nombre_csv, Modelo, mapeo_func, sql_template):
    """
    Migra los datos de una entidad especifica desde un archivo CSV,
    inserta los registros en la base de datos y genera el archivo SQL.
    """

    path_csv = os.path.join(carpeta_csv, nombre_csv)
    # Validacion de existencia del archivo CSV
    if not os.path.exists(path_csv):
        print(f"Saltando {nombre_csv}: archivo no encontrado.")
        return

    # Generacion del archivo SQL correspondiente
    with open(path_csv, 'r') as f, session_scope() as session:
        reader = csv.DictReader(f)
        nombre_tabla = nombre_csv.replace('.csv', '')
        sql_path = os.path.join(carpeta_sql, f'insert_{nombre_tabla}.sql')

        with open(sql_path, 'w') as sql_file:
            for row in reader:
                obj = mapeo_func(row)
                session.merge(obj)
                sql_file.write(sql_template.format(**row) + "\n")

    print(f"{nombre_csv} migrado correctamente.")
