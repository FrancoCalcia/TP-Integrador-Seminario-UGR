from functools import wraps
from datetime import datetime
from price_manager.database.connection import session_scope
from price_manager.models.models import Auditoria

def auditar(accion: str, detalle_func=None):
    """
    Decorador para auditar operaciones del sistema y registrarlas en la base de datos.
    
    Args:
        accion (str): Nombre de la acción realizada (ej: 'Ejecutar Scraping').
        detalle_func (callable, opcional): Función para generar dinámicamente el detalle a partir de los argumentos.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Ejecutar la función original
                resultado = func(*args, **kwargs)
                
                # Generar el detalle del log
                if detalle_func:
                    try:
                        detalle = detalle_func(*args, **kwargs)
                    except Exception:
                        detalle = f"Ejecución exitosa de {func.__name__}."
                else:
                    detalle = f"Ejecución exitosa de {func.__name__}."

                # Guardar en base de datos de forma autónoma
                with session_scope() as session:
                    log = Auditoria(
                        accion=accion,
                        fecha=datetime.now(),
                        detalle=detalle
                    )
                    session.add(log)
                
                return resultado
            except Exception as e:
                # Si falla, registrar el fallo en la auditoría
                with session_scope() as session:
                    log = Auditoria(
                        accion=accion,
                        fecha=datetime.now(),
                        detalle=f"FALLO en {func.__name__}: {str(e)}"
                    )
                    session.add(log)
                raise e
        return wrapper
    return decorator
