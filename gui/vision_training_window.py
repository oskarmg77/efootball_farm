# gui/vision_training_window.py

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Importamos las clases y configuraciones necesarias
from vision.action_monitor import ActionMonitor
from config.controls import KEYBOARD_MAPPING, GAMEPAD_MAPPING


class VisionTrainingWindow(tk.Toplevel):
    """
    Ventana para el entrenamiento asistido del modelo de visión.
    Permite al usuario mapear las pantallas del juego y las acciones para navegar entre ellas.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Entrenamiento del Módulo de Visión")
        self.geometry("800x600")

        # --- Estado y Lógica ---
        self.action_monitor = None
        self.is_session_active = False
        self.node_counter = 0

        self.protocol("WM_DELETE_WINDOW", self.on_close) # Manejar cierre de ventana

        # --- Frame Principal ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1) # Para que el log se expanda

        # --- Frame de Controles ---
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.start_session_button = ttk.Button(controls_frame, text="Iniciar Sesión de Entrenamiento", command=self.start_session)
        self.start_session_button.pack(side=tk.LEFT, padx=(0, 10))

        self.analyze_button = ttk.Button(controls_frame, text="Analizar Pantalla", command=self.analyze_screen, state="disabled")
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 10))

        self.save_map_button = ttk.Button(controls_frame, text="Guardar Mapa de Navegación", command=self.save_map, state="disabled")
        self.save_map_button.pack(side=tk.LEFT)

        # --- Log de la Sesión ---
        log_label = ttk.Label(main_frame, text="Log de la Sesión:")
        log_label.grid(row=1, column=0, sticky="w", pady=(10, 0))

        self.log_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=10)
        self.log_text.grid(row=2, column=0, sticky="nsew")
        self.log_text.configure(state='disabled') # Hacerlo de solo lectura

    def _log(self, message):
        """Añade un mensaje al área de log."""
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state='disabled')
        self.log_text.see(tk.END) # Auto-scroll


    def start_session(self):
        """Inicia una nueva sesión de entrenamiento."""
        self._log("INFO: Iniciando nueva sesión de entrenamiento.")
        self.is_session_active = True
        self.node_counter = 0

        # Inicializamos el monitor de acciones
        self.action_monitor = ActionMonitor(KEYBOARD_MAPPING, GAMEPAD_MAPPING)
        self._log("INFO: Monitor de acciones iniciado. Esperando primer análisis.")

        # Actualizamos la GUI
        self.start_session_button.config(state="disabled")
        self.analyze_button.config(state="normal")
        self.save_map_button.config(state="normal")

    def analyze_screen(self):
        """Analiza la pantalla actual, registra la acción previa y se prepara para la siguiente."""
        if not self.is_session_active:
            return

        # 1. Capturar la acción que nos trajo a esta pantalla
        captured_action = self.action_monitor.get_captured_action()

        # 2. Lógica de análisis de la pantalla (aquí irá la llamada a Gemini)
        # Por ahora, simulamos la creación de un nodo
        self.node_counter += 1
        current_node_id = f"Node-{self.node_counter}"
        self._log(f"ANALYSIS: Pantalla analizada. Creado {current_node_id}.")

        if captured_action:
            # Mensaje más claro para el usuario
            self._log(f"ACTION: La acción '{captured_action}' te trajo a esta pantalla.")
            # Aquí es donde crearíamos la arista en nuestro grafo de navegación
        else:
            self._log("ACTION: (Es la primera pantalla, no hay acción previa)")

        # 3. Prepararse para la siguiente acción
        self._log("LISTENING: Esperando la siguiente acción del usuario en el juego...")
        self.action_monitor.listen_for_single_action()

    def save_map(self):
        """Guarda el mapa de navegación generado."""
        self._log("SUCCESS: Mapa de navegación guardado (simulación).")
        messagebox.showinfo("Guardado", "El mapa de navegación se ha guardado correctamente (simulación).")

    def on_close(self):
        """Maneja el cierre de la ventana de forma segura."""
        if self.action_monitor:
            self.action_monitor.stop()
        self.destroy()