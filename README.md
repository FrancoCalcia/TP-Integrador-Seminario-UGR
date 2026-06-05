# Price Manager

Trabajo práctico integrador de la materia **Seminario de Actualización** (Universidad del Gran Rosario).

## Integrantes - Grupo 14

- Avecilla Tomás
- Bianciotto Franco
- Calcia Franco
- Crenna Giuliano
- Pace Bruno
- Zorzolo Rubio Juana

## Estado del Proyecto: Sprint 3

El proyecto se encuentra en el **Sprint 3**, incorporando persistencia en base de datos relacional (desarrollada en el Sprint 2) y agregando la extracción automatizada de precios de competidores mediante Web Scraping, generación de reportes analíticos y alertas, y control de auditoría general.

## Objetivo del Sprint 3

El objetivo principal de este sprint es integrar capacidades de inteligencia de precios mediante la obtención automatizada de datos de competidores web (específicamente del sitio de Star Computación) para comparar de forma automática con los precios internos del catálogo bimonetario.

Asimismo, se incorpora un motor de auditoría robusto por decoradores para trazar todas las acciones operativas críticas, la generación de reportes comparativos en formato Excel (`.xlsx`) y la exportación de archivos de alertas críticos en formato CSV ante desviaciones de precios que superen el umbral ingresado por el usuario.

## Introducción y Contexto del Trabajo

Debido a la volatilidad económica actual en Argentina, la distribuidora de hardware necesita actualizar rápidamente sus precios internos en base a las cotizaciones diarias del dólar y, al mismo tiempo, posicionar su rentabilidad frente a competidores directos del mercado de computación. 

Para lograr esto, en este Sprint:
1. **Extracción Web (Scrapy)**: Se realiza una búsqueda automatizada para cada producto registrado en el inventario interno sobre el sitio web de Star Computación, recopilando de forma inteligente descripciones, precios reales, formas de pago (contado/débito) y URLs de imágenes promocionales.
2. **Persistencia (SQLAlchemy)**: Los precios de competidores se almacenan directamente en la tabla relacional `precios_competencia`.
3. **Reportes y Alertas**: Se consolida un reporte ejecutivo Excel y alertas CSV para los productos que presenten diferencias críticas respecto al precio interno.
4. **Historial de Auditoría**: Cada ejecución y transacción crítica es automáticamente registrada utilizando un decorador `@auditar` y persistida en la tabla `auditoria`.

## Estructura de Directorios

```text
price_manager/
├── src/
│   └── price_manager/
│       ├── database/
│       │   └── connection.py  
│       ├── entities/
│       │   └── entities.py  
│       ├── models/
│       │   └── models.py  
│       ├── preload_data/
│       │   └── preload_data.py
│       ├── repositories/
│       │   └── repositories.py
│       ├── scraper/
│       │   ├── items.py
│       │   ├── pipelines.py
│       │   ├── spider.py
│       │   └── run_spider.py
│       ├── services/       
│       │   ├── report_service.py
│       │   ├── scraper_service.py
│       │   └── services.py
│       ├── migrations/
│       │   ├── csv/
│       │   │   └── table_name.csv
│       │   ├── sql/
│       │   │   └── table_name.sql
│       │   └── migrations.py
│       ├── ui/          
│       │   └── console.py
│       ├── utils/          
│       │   └── audit.py
│       └── main.py      
├── requirements.txt
├── CHANGELOG.md
└── README.md
```

## Requisitos

- Python 3.11 o superior
- Ver listado completo de paquetes necesarios en `requirements.txt` (incluye SQLAlchemy, Scrapy, pandas, openpyxl y python-dotenv).

## Ejecución del Programa

Desde la raíz del repositorio:

```bash
python ./price_manager/src/price_manager/main.py
```
