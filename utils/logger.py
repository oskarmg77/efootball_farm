import logging
import os

def setup_logger():
    """
    Configura y devuelve un logger para la aplicación.
    Los logs se guardarán en el directorio 'logs' y también se mostrarán en la consola.
    """
    # Nombre del logger para evitar conflictos con la librería
    logger = logging.getLogger('eFootballLogger')
    logger.setLevel(logging.DEBUG)  # Captura todos los niveles de logs

    # Si el logger ya tiene handlers, es porque ya fue configurado.
    if logger.hasHandlers():
        return logger

    # Crear el directorio 'logs' si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configurar el handler para el archivo
    file_handler = logging.FileHandler('logs/app.log', mode='w')
    file_handler.setLevel(logging.DEBUG)  # Guardar todos los logs desde DEBUG hacia arriba en el archivo

    # Configurar el handler para la consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Mostrar en consola solo desde INFO hacia arriba

    # Crear un formato para los logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Añadir los handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Crear una instancia única del logger para ser importada en otros módulos
log = setup_logger()
