
import os
import sys

# CONFIGURACIÓN DE RUTAS
# Aseguramos que las importaciones relativas funcionen correctamente al ejecutar main.py directamente
current_dir = os.path.dirname(os.path.abspath(__file__))
package_dir = os.path.abspath(os.path.join(current_dir, ".."))
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)


def main(import_default_data=False):
    """
    Función principal de ejecución de la aplicación.

    Args:
        import_default_data (bool):
            Parámetro reservado para futuras cargas
            automáticas de datos iniciales.
    """

    try:

        from price_manager.ui.console import ConsoleUI

        ui = ConsoleUI()

        ui.mostrar_menu()

    except Exception as error:

        print(
            f"Error crítico en la aplicación: {error}"
        )


# PUNTO DE ENTRADA PRINCIPAL
if __name__ == '__main__':

    main()