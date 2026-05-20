# Price Manager

## Sprint actual

Sprint 2

## Objetivo

El objetivo principal de este proyecto es aplicar los conocimientos adquiridos
en programación orientada a objetos, almacenamiento de datos en archivos para
su persistencia.

## Introducción y Contexto del problema

### Sprint 1

> Una empresa distribuidora de productos electrónicos necesita modernizar su
> sistema de gestión de inventarios. Debido a la volatilidad económica, el
> sistema debe gestionar precios en diferentes monedas y seguir de cerca la
> cotización del dólar para actualizar sus valores en tiempo real.
>
> El objetivo es desarrollar una aplicación de consola (CLI) robusta en Python
> que permita gestionar el inventario de un local de hardware, cotizar
> productos en tiempo real según el valor del dólar y comparar precios
> automáticamente con la competencia web.
>
> Descripción de las Entidades
> Para cumplir con el requerimiento, se han identificado las siguientes clases
> y sus restricciones:
>
> 1. Infraestructura de Catálogo y Logística
>
>    - Categoría: Define el rubro de los productos (ej: "Periféricos",
>      "Hardware"). Cada categoría tiene un identificador único numérico y un
>      nombre descriptivo.
>
>    - Proveedor: La entidad que nos provee la mercadería. Se debe registrar
>      su ID, nombre legal y una vía de contacto.
>
> 2. Gestión Económica (El módulo crítico)
>
>    - Precio: No es un simple número. Es un objeto que contiene el valor
>      (no puede ser negativo), la moneda (usando el código internacional de
>      3 letras, ej: ARS, USD) y la fecha de última actualización.
>
>    - CotizaciónDolar: Para proteger la rentabilidad, el sistema debe
>      registrar la cotización diaria. Se debe indicar el valor (siempre
>      positivo), la fecha y el tipo (ej: "Oficial", "Blue", "Tarjeta").
>
> 3. Núcleo del Negocio
>
>    - Producto: Es el centro del sistema. Cada producto tiene un ID, nombre
>      y descripción. Lo más importante: cada producto está asociado a una
>      instancia de Precio, una Categoría y un Proveedor.
>
>    - Stock: Esta clase vincula un Producto con un Almacén específico,
>      indicando la cantidad disponible (la cual nunca puede ser menor a cero).
>
> El trabajo simulará un entorno de desarrollo real, incremental y
> colaborativo.

### Sprint 2

En esta segunda entrega vamos a ampliar el alcance haciendo que la aplicación
persista en una base de datos relacional. Para este caso vamos a utilizar el
ORM SQLAlchemy.

La idea principal es realizar una migración de todos los datos cargados en los
archivos a tablas relacionales.

El objetivo principal es consolidar las bases de manejo de bases de datos,
normalización, conexión segura y carga inicial.

Además realizaremos consultas a APIs externas.

Para todo esto debemos partir del último push que se realizó en la entrega 1.
