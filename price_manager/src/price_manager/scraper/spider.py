import scrapy
import urllib.parse
from price_manager.scraper.items import ProductoWebItem
from scrapy.loader import ItemLoader

class StarComputacionSpider(scrapy.Spider):
    name = 'star_computacion'
    allowed_domains = ['starcomputacion.com.ar']

    def __init__(self, *args, **kwargs):
        super(StarComputacionSpider, self).__init__(*args, **kwargs)
        
        # Obtener los productos desde la base de datos
        from price_manager.database.connection import session_scope
        from price_manager.repositories.repositories import ProductoRepository
        
        self.start_urls = []
        self.producto_map = {}

        with session_scope() as session:
            repo = ProductoRepository(session)
            productos = repo.get_all()
            for prod in productos:
                query = urllib.parse.quote(prod.nombre)
                url = f'https://www.starcomputacion.com.ar/prods/search/?search={query}'
                self.start_urls.append(url)
                # Mapear URL para recuperar metadatos en el parse
                self.producto_map[url] = {
                    'id': prod.id,
                    'nombre': prod.nombre
                }
        print(f'>>> SPIDER INICIALIZADA CON {len(self.start_urls)} URLS DE BUSQUEDA <<<', flush=True)

    def parse(self, response):
        # Buscar info de producto correspondiente al URL
        prod_info = self.producto_map.get(response.url)
        if not prod_info:
            # Buscar coincidencia parcial si hubo redirección
            for url_key, info in self.producto_map.items():
                if urllib.parse.unquote(response.url) in urllib.parse.unquote(url_key) or urllib.parse.unquote(url_key) in urllib.parse.unquote(response.url):
                    prod_info = info
                    break

        if not prod_info:
            # Fallback a primer producto si no coincide
            prod_info = list(self.producto_map.values())[0] if self.producto_map else {'id': 1, 'nombre': 'Desconocido'}

        producto_interno_id = prod_info['id']
        producto_interno_nombre = prod_info['nombre']

        print(f'>>> PARSE BUSQUEDA PARA {producto_interno_nombre} <<<', flush=True)

        # Encontrar los cards de productos
        products = response.css('a.product')
        # Limitar a los 10 primeros resultados
        products = products[:10]

        if not products:
            self.log(f'No se encontraron resultados para: {producto_interno_nombre}')
            return

        for p in products:
            href = p.css('::attr(href)').get()
            title = p.css('.title::text').get()
            price = p.css('.price::text').get()
            img_src = p.css('img.img::attr(src)').get()

            # Resolver URL absoluta de la imagen y detalle
            if img_src:
                abs_img_url = img_src if img_src.startswith('http') else f'https://www.starcomputacion.com.ar/{img_src.lstrip("/")}'
            else:
                abs_img_url = None

            if href:
                orig_detail_url = href if href.startswith('http') else f'https://www.starcomputacion.com.ar/{href.lstrip("/")}'
                
                yield scrapy.Request(
                    url=orig_detail_url,
                    callback=self.parse_detail,
                    meta={
                        'producto_interno_id': producto_interno_id,
                        'producto_interno_nombre': producto_interno_nombre,
                        'nombre_web': title,
                        'precio_web': price,
                        'imagen_url': abs_img_url
                    }
                )

    def parse_detail(self, response):
        producto_interno_id = response.meta['producto_interno_id']
        producto_interno_nombre = response.meta['producto_interno_nombre']
        nombre_web = response.meta['nombre_web']
        precio_web = response.meta['precio_web']
        imagen_url = response.meta['imagen_url']

        print(f'>>> PARSE DETALLE: {nombre_web} ({precio_web}) <<<', flush=True)

        loader = ItemLoader(item=ProductoWebItem(), response=response)
        loader.add_value('producto_interno_id', producto_interno_id)
        loader.add_value('producto_interno_nombre', producto_interno_nombre)
        loader.add_value('nombre_web', nombre_web)
        loader.add_value('precio_web', precio_web)
        loader.add_value('imagen_url', imagen_url)

        # Descripción detallada
        loader.add_css('descripcion_web', '#product_desc ::text, .desc_general ::text')

        # Formas de pago
        formas_pago = {}
        rows = response.css('#prices_table tr')
        for row in rows:
            tds = row.css('td')
            if len(tds) >= 2:
                metodo = tds[0].css('::text').get()
                valor_pago = tds[1].css('::text').get()
                if metodo and valor_pago:
                    formas_pago[metodo.strip()] = valor_pago.strip()

        # Si no hay tabla de precios, crear una forma de pago simple de contado
        if not formas_pago and precio_web:
            formas_pago['CONTADO'] = precio_web.strip()

        item = loader.load_item()
        item['formas_pago'] = formas_pago

        yield item
