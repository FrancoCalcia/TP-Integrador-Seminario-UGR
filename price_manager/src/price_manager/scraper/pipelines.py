import json
from price_manager.database.connection import session_scope
from price_manager.models.models import PrecioCompetencia

class PrecioCompetenciaPipeline:
    def process_item(self, item, spider):
        # Convertir formas_pago (dict/list) a JSON para persistencia
        formas_pago_json = None
        if item.get('formas_pago'):
            try:
                formas_pago_json = json.dumps(item['formas_pago'], ensure_ascii=False)
            except Exception:
                formas_pago_json = str(item['formas_pago'])

        # Guardar en base de datos
        with session_scope() as session:
            db_item = PrecioCompetencia(
                producto_interno_id=item.get('producto_interno_id'),
                nombre_web=item.get('nombre_web', 'Desconocido'),
                precio_web=item.get('precio_web', 0.0),
                imagen_url=item.get('imagen_url'),
                descripcion_web=item.get('descripcion_web'),
                formas_pago=formas_pago_json
            )
            session.add(db_item)
        return item
