# La clase base de la que heredarán todas las ventanas.
# gui/base_window.py

import customtkinter as ctk

class BaseWindow(ctk.CTkToplevel):
    def __init__(self, title="Ventana de Prueba", width=400, height=300, resizable=True):
        super().__init__()

        # --- Configuración de la Apariencia ---
        ctk.set_appearance_mode("dark")  # "dark", "light", "system"
        ctk.set_default_color_theme("blue")

        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(resizable, resizable)

        # Centrar la ventana (opcional pero recomendable)
        self.after(250, lambda: self.center_window(width, height))

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))