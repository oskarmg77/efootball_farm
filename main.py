# main.py
from gui.main_window import MainWindow
from utils.logger import log

def main():
    """Función principal para iniciar la aplicación."""
    log.info('Iniciando la aplicación')
    try:
        app = MainWindow()
        app.mainloop()
        log.info('La aplicación se ha cerrado correctamente')
    except Exception as e:
        log.error('Ha ocurrido un error inesperado', exc_info=True)

if __name__ == "__main__":
    main()
