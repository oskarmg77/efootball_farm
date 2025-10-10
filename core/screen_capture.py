import pygetwindow as gw
from PIL import ImageGrab
import platform


def capture_window(window_title: str = "eFootball™ 2024"):
    """
    Captura el contenido de una ventana específica por su título.

    Args:
        window_title (str): El título de la ventana a capturar.

    Returns:
        Image.Image | None: Un objeto de imagen de Pillow si la ventana se encuentra,
                            de lo contrario None.
    """
    try:
        # En Windows, pygetwindow funciona muy bien. En otros SO, puede ser menos fiable.
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            print(f"Error: No se encontró ninguna ventana con el título '{window_title}'.")
            return None

        window = windows[0]
        # Asegurarse de que la ventana esté activa (opcional, pero recomendado)
        if platform.system() == "Windows" and not window.isActive:
            window.activate()

        # Capturar la región de la ventana
        bbox = (window.left, window.top, window.right, window.bottom)
        screenshot = ImageGrab.grab(bbox)
        return screenshot

    except Exception as e:
        print(f"Ocurrió un error al capturar la ventana: {e}")
        return None