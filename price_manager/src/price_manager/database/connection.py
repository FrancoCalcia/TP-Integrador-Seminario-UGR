
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# DEFINICIÓN DE LA BASE DECLARATIVA
# Base utilizada por SQLAlchemy para la creación de modelos ORM
Base = declarative_base()

# Ruta de la base de datos SQLite utilizada por el proyecto
import os
from pathlib import Path
if os.path.exists('/content'):
    DB_PATH = "/content/TP-Integrador-Seminario-UGR/price_manager/price_manager.db"
else:
    DB_PATH = str(Path(__file__).resolve().parents[2] / "price_manager.db")



class ConexionDB:
    """Clase encargada de administrar la conexión y las sesiones de la base de datos mediante SQLAlchemy"""

    def __init__(self, db_url=f"sqlite:///{DB_PATH}"):

        try:
            self.engine = create_engine(db_url, echo=False)

            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )

        except Exception as error:
            print(f"Error al conectar con la base de datos: {error}")

    def get_session(self):
        """
        Genera y retorna una nueva sesión de base de datos.

        Returns:
            Session: Sesión activa de SQLAlchemy.
        """
        return self.SessionLocal()


# Instancia global reutilizable dentro del proyecto
db_manager = ConexionDB()
# CONTEXT MANAGER PARA TRANSACCIONES
# Permite administrar automáticamente la apertura, confirmación y cierre de sesiones de base de datos
@contextmanager
def session_scope():
    """ Context manager para manejar transacciones de forma segura utilizando SQLAlchemy"""

    session = db_manager.get_session()

    try:
        yield session
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error en la transacción: {e}")
        raise

    finally:
        session.close()