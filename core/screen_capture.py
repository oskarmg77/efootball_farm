import pygetwindow as gw
from PIL import ImageGrab
import platform
import customtkinter as ctk
from config.settings import GAME_WINDOW_TITLE


class RegionSelector(ctk.CTkToplevel):
    """
    Una ventana de superposición para que el usuario seleccione una región de la pantalla.
    """
    def __init__(self):
        super().__init__()
        self.withdraw() # Ocultar la ventana al inicio

        # Configuración para que ocupe toda la pantalla y sea semitransparente
        self.attributes("-fullscreen", True)
        self.attributes("-alpha", 0.3)
        self.configure(fg_color="black")
        self.protocol("WM_DELETE_WINDOW", self.cancel_selection)

        self.canvas = ctk.CTkCanvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.bbox = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind("<Escape>", self.cancel_selection)

        self.deiconify() # Mostrar la ventana
        self.lift()
        self.focus_force()

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        cur_x, cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.bbox = (min(self.start_x, end_x), min(self.start_y, end_y), max(self.start_x, end_x), max(self.start_y, end_y))
        self.destroy()

    def cancel_selection(self, event=None):
        self.bbox = None
        self.destroy()


def capture_window():
    """
    Captura el contenido de una ventana específica utilizando el título definido en `config/settings.py`.
    Busca una coincidencia parcial del título para mayor robustez.

    Returns:
        Image.Image | None: Un objeto de imagen de Pillow si la ventana se encuentra,
                            de lo contrario None.
    """
    try:
        target_window = None
        # Busca una ventana cuyo título contenga el título del juego.
        all_windows = gw.getAllWindows()
        for window in all_windows:
            if GAME_WINDOW_TITLE in window.title:
                target_window = window
                break

        if not target_window:
            print(f"Error: No se encontró ninguna ventana que contenga el título '{GAME_WINDOW_TITLE}'.")
            return None

        # Asegurarse de que la ventana esté activa (opcional, pero recomendado para Windows)
        if platform.system() == "Windows" and not target_window.isActive:
            try:
                target_window.activate()
            except Exception:
                # A veces la activación puede fallar si la ventana está minimizada
                target_window.restore()
                target_window.activate()

        # Capturar la región de la ventana
        bbox = (target_window.left, target_window.top, target_window.right, target_window.bottom)
        screenshot = ImageGrab.grab(bbox)
        return screenshot

    except Exception as e:
        print(f"Ocurrió un error inesperado durante la captura de pantalla: {e}")
        return None


def capture_region_interactive() -> ImageGrab.Image | None:
    """
    Permite al usuario seleccionar interactivamente una región de la pantalla y la captura.

    Returns:
        Image.Image | None: Un objeto de imagen de Pillow con la región capturada, o None si se cancela.
    """
    selector = RegionSelector()
    selector.wait_window() # Espera hasta que la ventana del selector se cierre

    bbox = selector.bbox
    if bbox:
        print(f"Región seleccionada: {bbox}")
        return ImageGrab.grab(bbox)
    else:
        print("Captura de región cancelada.")
        return None