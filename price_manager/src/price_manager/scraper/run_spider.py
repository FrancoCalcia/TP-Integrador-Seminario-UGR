import sys
import os
import asyncio

# Configurar el event loop de asyncio para Windows antes de importar Scrapy/Twisted
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Configurar PYTHONPATH para que Scrapy encuentre los módulos del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from scrapy.crawler import CrawlerProcess
from price_manager.scraper.spider import StarComputacionSpider

print("DEBUG: Spider is imported from:", sys.modules[StarComputacionSpider.__module__].__file__, flush=True)

def run():
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'ITEM_PIPELINES': {
            'price_manager.scraper.pipelines.PrecioCompetenciaPipeline': 300,
        },
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(StarComputacionSpider)
    process.start()

if __name__ == '__main__':
    run()
