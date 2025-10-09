# La interfaz principal del programa.
# gui/main_window.py

import customtkinter as ctk
from .base_window import BaseWindow
from .input_test_window import InputTestWindow  # Para poder abrir la otra ventana


class MainWindow(ctk.CTk):  # La ventana principal hereda directamente de CTk
    def __init__(self):
        super().__init__()

        # --- Configuración ---
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("eFootball Automator - Gemini Agent")
        self.geometry("800x600")

        # --- Layout Principal (2 columnas) ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Columna Izquierda (Navegación y Controles) ---
        nav_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        nav_frame.grid(row=0, column=0, sticky="nsw")

        nav_title = ctk.CTkLabel(nav_frame, text="Panel de Control", font=ctk.CTkFont(size=20, weight="bold"))
        nav_title.pack(pady=20, padx=20)

        btn_start = ctk.CTkButton(nav_frame, text="Iniciar Bot", height=40)
        btn_start.pack(pady=10, padx=20, fill="x")

        btn_stop = ctk.CTkButton(nav_frame, text="Detener Bot", height=40, fg_color="red", hover_color="#8B0000")
        btn_stop.pack(pady=10, padx=20, fill="x")

        # Separador visual
        separator = ctk.CTkFrame(nav_frame, height=2, fg_color="gray")
        separator.pack(pady=20, padx=20, fill="x")

        # Botón para abrir la ventana de pruebas
        btn_open_test_window = ctk.CTkButton(nav_frame, text="Probar Controles", command=self.open_input_tester)
        btn_open_test_window.pack(pady=10, padx=20, fill="x")

        # --- Columna Derecha (Información y Logs) ---
        main_content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        main_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Aquí iría el visor de la pantalla del juego, el log, etc.
        log_textbox = ctk.CTkTextbox(main_content_frame, state="disabled")  # Para mostrar logs
        log_textbox.pack(fill="both", expand=True)

    def open_input_tester(self):
        # Esta función crea y muestra la ventana de prueba
        input_window = InputTestWindow()
        input_window.grab_set()  # Hace que la ventana de prueba sea modal (bloquea la principal)