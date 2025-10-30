# La clase base de la que heredarán todas las ventanas.
# gui/base_window.py

import customtkinter as ctk

class BaseWindow(ctk.CTk):
    """Clase base para la ventana principal de la aplicación."""
    def __init__(self, title="eFootball Farm", width=500, height=400, resizable=False):
        super().__init__()

        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(resizable, resizable)

        # Centrar la ventana (opcional pero recomendable)
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

class BaseToplevelWindow(ctk.CTkToplevel):
    """Clase base para ventanas secundarias (Toplevel)."""
    def __init__(self, title="Ventana Secundaria", width=500, height=400, resizable=False):
        super().__init__()

        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(resizable, resizable)

        # Centrar la ventana (opcional pero recomendable)
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))