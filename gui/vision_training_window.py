# gui/vision_training_window.py

import customtkinter as ctk
from tkinter import messagebox

# Importamos las clases y configuraciones necesarias
from vision.action_monitor import ActionMonitor
from config.controls import KEYBOARD_MAPPING, GAMEPAD_MAPPING
from core.screen_capture import capture_window, capture_region_interactive


class VisionTrainingWindow(ctk.CTkToplevel):
    """
    Ventana para el entrenamiento asistido del modelo de visión.
    Permite al usuario mapear las pantallas del juego y las acciones para navegar entre ellas.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Entrenamiento del Módulo de Visión")
        self.geometry("800x650")
        self.resizable(True, True)

        # --- Estado y Lógica ---
        self.action_monitor = None
        self.is_session_active = False
        self.node_counter = 0

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- Frame Principal ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Panel de Instrucciones Dinámico ---
        self.instructions_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#334257")
        self.instructions_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.instructions_frame.grid_columnconfigure(0, weight=1)

        self.instructions_label = ctk.CTkLabel(self.instructions_frame, text="", font=ctk.CTkFont(size=14), wraplength=700)
        self.instructions_label.grid(row=0, column=0, padx=20, pady=15, sticky="ew")

        # --- Frame de Controles ---
        controls_frame = ctk.CTkFrame(self)
        controls_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.start_session_button = ctk.CTkButton(controls_frame, text="Iniciar Sesión de Entrenamiento", command=self.start_session)
        self.start_session_button.pack(side="left", padx=10, pady=10)

        self.analyze_button = ctk.CTkButton(controls_frame, text="Analizar Pantalla", command=self.analyze_screen, state="disabled")
        self.analyze_button.pack(side="left", padx=10, pady=10)

        self.analyze_region_button = ctk.CTkButton(controls_frame, text="Analizar Región...", command=lambda: self.analyze_screen(is_region=True), state="disabled", fg_color="#1F618D")
        self.analyze_region_button.pack(side="left", padx=10, pady=10)

        self.save_map_button = ctk.CTkButton(controls_frame, text="Guardar Mapa de Navegación", command=self.save_map, state="disabled")
        self.save_map_button.pack(side="left", padx=10, pady=10)

        # --- Log de la Sesión ---
        log_frame = ctk.CTkFrame(self)
        log_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        self.log_text = ctk.CTkTextbox(log_frame, wrap="word", state="disabled")
        self.log_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Estado inicial
        self._update_instructions("info", "Haz clic en 'Iniciar Sesión' para comenzar el proceso de mapeo de pantallas.")

    def _log(self, message):
        """Añade un mensaje al área de log."""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.configure(state="disabled")
        self.log_text.see("end")

    def _update_instructions(self, state, text):
        """Actualiza el panel de instrucciones con un color y texto específicos."""
        colors = {
            "info": "#334257",      # Azul oscuro
            "action_needed": "#FFC107", # Amarillo/Ámbar
            "listening": "#2E7D32"      # Verde oscuro
        }
        text_colors = {
            "info": "white",
            "action_needed": "black",
            "listening": "white"
        }
        self.instructions_frame.configure(fg_color=colors.get(state, "gray"))
        self.instructions_label.configure(text=text, text_color=text_colors.get(state, "white"))

    def start_session(self):
        """Inicia una nueva sesión de entrenamiento."""
        self._log("INFO: Iniciando nueva sesión de entrenamiento.")
        self.is_session_active = True
        self.node_counter = 0
        self.action_monitor = ActionMonitor(KEYBOARD_MAPPING, GAMEPAD_MAPPING)
        self._log("INFO: Monitor de acciones iniciado. Esperando primer análisis.")

        # Actualizamos la GUI
        self.start_session_button.configure(state="disabled")
        self.analyze_button.configure(state="normal")
        self.analyze_region_button.configure(state="normal")
        self.save_map_button.configure(state="normal")
        self._update_instructions(
            "action_needed",
            "PASO 1: Ve a la primera pantalla del juego que quieras mapear. Cuando estés listo, vuelve y haz clic en 'Analizar Pantalla Completa' o 'Analizar Región'."
        )

    def analyze_screen(self, is_region: bool = False):
        """Analiza la pantalla actual, registra la acción previa y se prepara para la siguiente."""
        if not self.is_session_active:
            return

        # 1. Capturar la acción que nos trajo a esta pantalla
        captured_action = self.action_monitor.get_captured_action() # Esto es seguro, devuelve None si no hay nada
        
        # Ocultar temporalmente la GUI para no interferir con la captura
        self.withdraw()
        self.after(200) # Pequeña pausa para que la ventana se oculte

        # 2. Capturar la imagen (pantalla completa o región)
        if is_region:
            self._log("INFO: Iniciando captura de región. Dibuja un rectángulo en la pantalla.")
            image = capture_region_interactive()
        else:
            image = capture_window()
        
        # Volver a mostrar la GUI
        self.deiconify()

        if image is None:
            self._log("ERROR: La captura de pantalla fue cancelada o falló.")
            return

        # 3. Lógica de análisis de la pantalla (aquí irá la llamada a Gemini con la 'image')
        # Por ahora, simulamos la creación de un nodo
        self.node_counter += 1
        current_node_id = f"Node-{self.node_counter}"
        analysis_type = "Región" if is_region else "Pantalla completa"
        self._log(f"ANALYSIS: {analysis_type} analizada. Creado {current_node_id}.")

        if captured_action:
            # Mensaje más claro para el usuario
            self._log(f"ACTION: La acción '{captured_action}' te trajo a esta pantalla.")
            # Aquí es donde crearíamos la arista en nuestro grafo de navegación
        else:
            self._log("ACTION: (Es la primera pantalla, no hay acción previa)")

        # 4. Prepararse para la siguiente acción
        self.analyze_button.configure(state="disabled") # Desactivar botón mientras se escucha
        self.analyze_region_button.configure(state="disabled")
        self._update_instructions(
            "listening",
            "PASO 2: ¡Escuchando! Ahora ve al juego y realiza UNA SOLA ACCIÓN para ir a la siguiente pantalla (ej. pulsar 'Enter', 'Abajo'...). La acción se registrará automáticamente."
        )
        self.update_idletasks() # Forzar actualización de la GUI

        self._log("LISTENING: Esperando la siguiente acción del usuario en el juego...")
        self.action_monitor.listen_for_single_action()
        self.after(500, self.check_if_action_captured)

    def save_map(self):
        """Guarda el mapa de navegación generado."""
        self._log("SUCCESS: Mapa de navegación guardado (simulación).")
        messagebox.showinfo("Guardado", "El mapa de navegación se ha guardado correctamente (simulación).")

    def on_close(self):
        """Maneja el cierre de la ventana de forma segura."""
        if self.action_monitor:
            self.action_monitor.stop()
        self.destroy()

    def check_if_action_captured(self):
        """Comprueba periódicamente si el monitor ha capturado una acción."""
        if self.action_monitor and self.action_monitor.last_action is not None:
            self.analyze_button.configure(state="normal")
            self.analyze_region_button.configure(state="normal")
            self._update_instructions(
                "action_needed",
                f"¡Acción '{self.action_monitor.last_action}' registrada! Ahora, vuelve a hacer clic en 'Analizar Pantalla' para confirmar la nueva pantalla."
            )
        elif self.is_session_active:
            self.after(500, self.check_if_action_captured)