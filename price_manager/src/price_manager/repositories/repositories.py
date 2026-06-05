from sqlalchemy.orm import Session
from price_manager.models.models import (
    Categoria,
    Producto,
    Proveedor
)

# REPOSITORIO DE PRODUCTOS
# Encapsula las operaciones de acceso a datos relacionadas con la entidad Producto
class ProductoRepository:

    def __init__(self, session: Session):
        """
        Inicializa el repositorio con una sesión activa de SQLAlchemy.

        Args:
            session (Session): Sesión de base de datos.
        """
        self.session = session

    def get_all(self):
        """
        Obtiene todos los productos almacenados en la base de datos.

        Returns:
            list[Producto]: Lista de productos.
        """
        return self.session.query(Producto).all()

    def get_by_id(self, id: int):
        """
        Obtiene un producto a partir de su identificador.

        Args:
            id (int): Identificador del producto.

        Returns:
            Producto | None: Producto encontrado o None.
        """
        return self.session.query(Producto).filter(
            Producto.id == id
        ).first()

    def add(self, producto: Producto):
        """
        Agrega un nuevo producto a la sesión actual.

        Args:
            producto (Producto): Producto a almacenar.
        """
        self.session.add(producto)

# REPOSITORIO DE CATEGORÍAS
# Gestiona las operaciones de acceso a datos
# vinculadas con la entidad Categoria.
class CategoriaRepository:

    def __init__(self, session: Session):
        """
        Inicializa el repositorio con una sesión activa de SQLAlchemy.

        Args:
            session (Session): Sesión de base de datos.
        """
        self.session = session

    def get_all(self):
        """
        Obtiene todas las categorías registradas.

        Returns:
            list[Categoria]: Lista de categorías.
        """
        return self.session.query(Categoria).all()


# REPOSITORIO DE PROVEEDORES
# Gestiona las operaciones de acceso a datos relacionadas con la entidad Proveedor
class ProveedorRepository:

    def __init__(self, session: Session):
        """
        Inicializa el repositorio con una sesión activa de SQLAlchemy.

        Args:
            session (Session): Sesión de base de datos.
        """
        self.session = session

    def get_all(self):
        """
        Obtiene todos los proveedores registrados.

        Returns:
            list[Proveedor]: Lista de proveedores.
        """
        return self.session.query(Proveedor).all()