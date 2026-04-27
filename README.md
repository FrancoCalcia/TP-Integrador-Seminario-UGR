# Price Manager

Trabajo práctico integrador de la materia **Seminario de Actualización**
(Universidad del Gran Rosario).

## Integrantes

- Franco Calcia
- Juana Zorzolo
- Bruno Pace
- Franco Bianciotto
- Giuliano Crenna
- Tomás Avecilla

## Estado del proyecto

Sprint 1 con estructura base, entidades, repositorios, servicios, precarga de
datos y aplicación de consola (CLI) con menú principal.

## Objetivo

Desarrollar una aplicación de consola en Python para gestionar:

- Categorías
- Proveedores
- Monedas
- Productos
- Stock
- Cotizaciones del dólar

## Estructura principal

```text
price_manager/
└── src/
    └── price_manager/
        ├── entities/
        │   └── entities.py
        ├── repositories/
        │   └── repositories.py
        ├── services/
        │   └── services.py
        ├── preload_data/
        │   └── preload_data.py
        ├── migrations/
        │   └── csv/
        ├── ui/
        │   └── console.py
        └── main.py
```

## Requisitos

- Python 3.11 o superior

## Ejecución

Desde la raíz del repositorio:

```bash
python .\price_manager\src\price_manager\main.py
```

La app inicia con precarga de datos desde `migrations/csv` y muestra el menú de
consola.

## Librerías permitidas
- traceback
- random
- keyword
- collection
- asyncio
- nest_asyncio
- sys
- importlib
- time
- math
- cmath
- typing
- enum
- functools
- operator
- abc
- dataclasses
- attr
- pydantic
- datetime
- uuid
- pydantic_settings
- contextlib
- configparser
- yaml
- xml
- csv
- json

