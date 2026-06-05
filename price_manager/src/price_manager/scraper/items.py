import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def clean_price(value):
    if not value:
        return 0.0
    # Remover símbolos, espacios, separadores de miles y dejar solo números y punto/coma
    cleaned = "".join(c for c in value if c.isdigit() or c in ['.', ','])
    if not cleaned:
        return 0.0
    # Formatear coma decimal
    if ',' in cleaned and '.' in cleaned:
        cleaned = cleaned.replace('.', '').replace(',', '.')
    elif ',' in cleaned:
        cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def clean_text(value):
    if not value:
        return ""
    return value.strip()

class ProductoWebItem(scrapy.Item):
    producto_interno_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    producto_interno_nombre = scrapy.Field(
        output_processor=TakeFirst()
    )
    nombre_web = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    precio_web = scrapy.Field(
        input_processor=MapCompose(clean_price),
        output_processor=TakeFirst()
    )
    imagen_url = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    formas_pago = scrapy.Field(
        output_processor=TakeFirst()
    )
    descripcion_web = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
