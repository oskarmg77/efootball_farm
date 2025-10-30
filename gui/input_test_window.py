# La ventana de prueba para el gamepad/teclado.
# gui/input_test_window.py

import time
import customtkinter as ctk
from .base_window import BaseToplevelWindow  # Cambiado a BaseToplevelWindow
from core.input_controller import execute_action
from config import controls
from config.controls import (
    MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, CONFIRM, BACK, PAUSE_MENU,
    SPRINT, PASS_SHORT, PASS_HIGH, PASS_THROUGH, SHOOT,
    CHANGE_PLAYER, CALL_SECOND_DEFENDER
)


class InputTestWindow(BaseToplevelWindow):  # Cambiado a BaseToplevelWindow
    def __init__(self):
        # Llamamos al constructor de la clase base con sus parámetros
        super().__init__(title="Simulador de Controles", width=800, height=500)

        # Variable para almacenar el esquema de control actual
        self.current_scheme = ctk.StringVar(value="Teclado")
        self.current_scheme.trace_add("write", self.update_button_labels)

        # Almacenaremos los botones para poder actualizar sus etiquetas
        self.action_buttons = []
        # --- Frame Principal ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- Panel de Control (Izquierda) ---
        control_panel = ctk.CTkFrame(self, corner_radius=10)
        control_panel.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        # --- Título ---
        title_label = ctk.CTkLabel(control_panel, text="Simulador de Acciones", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 15), padx=10)

        # --- Selector de modo (Teclado/Gamepad) ---
        scheme_frame = ctk.CTkFrame(control_panel, fg_color="transparent")
        scheme_frame.pack(pady=10)
        ctk.CTkLabel(scheme_frame, text="Modo:").pack(side="left", padx=5)
        ctk.CTkRadioButton(scheme_frame, text="Teclado", variable=self.current_scheme, value="Teclado").pack(side="left")
        ctk.CTkRadioButton(scheme_frame, text="Gamepad", variable=self.current_scheme, value="Gamepad").pack(side="left", padx=10)

        # --- Contenedor para todos los botones de acción ---
        actions_container = ctk.CTkScrollableFrame(control_panel, label_text="Acciones del Juego")
        actions_container.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Navegación ---
        self._create_button(actions_container, "Confirmar", CONFIRM, {"fg_color": "green", "hover_color": "#006400"})
        self._create_button(actions_container, "Atrás", BACK, {"fg_color": "red", "hover_color": "#8B0000"})
        self._create_button(actions_container, "Pausa", PAUSE_MENU)

        # --- D-Pad ---
        dpad_frame = ctk.CTkFrame(actions_container)
        dpad_frame.pack(pady=(15, 10))
        self._create_dpad_button(dpad_frame, "▲", MOVE_UP).grid(row=0, column=1, padx=5, pady=5)
        self._create_dpad_button(dpad_frame, "◀", MOVE_LEFT).grid(row=1, column=0, padx=5, pady=5)
        self._create_dpad_button(dpad_frame, "▶", MOVE_RIGHT).grid(row=1, column=2, padx=5, pady=5)
        self._create_dpad_button(dpad_frame, "▼", MOVE_DOWN).grid(row=2, column=1, padx=5, pady=5)

        # --- Acciones de Ataque ---
        attack_frame = ctk.CTkFrame(actions_container, fg_color="transparent")
        attack_frame.pack(pady=10, fill="x")
        ctk.CTkLabel(attack_frame, text="--- Ataque ---", font=ctk.CTkFont(slant="italic")).pack()
        self._create_button(attack_frame, "Sprint", SPRINT)
        self._create_button(attack_frame, "Disparo", SHOOT)
        self._create_button(attack_frame, "Pase Corto", PASS_SHORT)
        self._create_button(attack_frame, "Pase Largo", PASS_HIGH)
        self._create_button(attack_frame, "Pase Profundo", PASS_THROUGH)

        # --- Acciones de Defensa ---
        defense_frame = ctk.CTkFrame(actions_container, fg_color="transparent")
        defense_frame.pack(pady=10, fill="x")
        ctk.CTkLabel(defense_frame, text="--- Defensa ---", font=ctk.CTkFont(slant="italic")).pack()
        self._create_button(defense_frame, "Cambiar Jugador", CHANGE_PLAYER)
        self._create_button(defense_frame, "Llamar 2º Defensor", CALL_SECOND_DEFENDER)

        # --- Panel de Registro (Derecha) ---
        log_panel = ctk.CTkFrame(self, corner_radius=10)
        log_panel.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        log_panel.grid_rowconfigure(0, weight=1)
        log_panel.grid_columnconfigure(0, weight=1)

        self.log_textbox = ctk.CTkTextbox(log_panel, wrap="word", state="disabled")
        self.log_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self._log("Simulador iniciado. Selecciona un modo y una acción.", "white")
        self._log("ADVERTENCIA: Las acciones se ejecutarán en la ventana activa tras 3 segundos.", "orange")

        # Actualizar etiquetas de botones al iniciar
        self.update_button_labels()

    def _create_button(self, parent, text, action, options=None):
        """Función de ayuda para crear y registrar un botón de acción."""
        options = options or {}
        button = ctk.CTkButton(parent, text=text, command=lambda: self.on_button_click(action), **options)
        button.pack(fill="x", pady=4, padx=10)
        self.action_buttons.append({"widget": button, "base_text": text, "action": action})

    def _create_dpad_button(self, parent, text, action):
        button = ctk.CTkButton(parent, text=text, width=50, command=lambda: self.on_button_click(action))
        self.action_buttons.append({"widget": button, "base_text": text, "action": action})
        return button

    def on_button_click(self, action: str):
        """Llama a la lógica del controlador y muestra el resultado."""
        self._log(f"Ejecutando '{action}' en 3 segundos...", "cyan")
        self.update() # Forzar actualización de la GUI
        time.sleep(3)

        active_scheme = controls.KEYBOARD_MAPPING if self.current_scheme.get() == "Teclado" else controls.GAMEPAD_MAPPING
        message = execute_action(action, active_scheme)
        
        color = "red" if "Error" in message else "lightgreen"
        self._log(message, color)

    def _log(self, message: str, color: str):
        """Añade un mensaje al log con un color específico."""
        self.log_textbox.configure(state="normal")
        timestamp = time.strftime('%H:%M:%S')
        self.log_textbox.insert("end", f"[{timestamp}] {message}\n")
        self.log_textbox.configure(state="disabled")
        self.log_textbox.see("end")

    def update_button_labels(self, *args):
        """Actualiza el texto de los botones para mostrar la tecla/botón correspondiente."""
        is_gamepad = self.current_scheme.get() == "Gamepad"
        active_scheme = controls.GAMEPAD_MAPPING if is_gamepad else controls.KEYBOARD_MAPPING

        # Mapeo de nombres internos a nombres amigables para el usuario
        gamepad_name_map = {
            'button_south': 'A', 'button_east': 'B', 'button_west': 'X', 'button_north': 'Y',
            'left_bumper': 'LB', 'right_bumper': 'RB',
            'left_trigger': 'LT', 'right_trigger': 'RT',
            'start_button': 'Start',
            'dpad_up': '↑', 'dpad_down': '↓', 'dpad_left': '←', 'dpad_right': '→',
        }

        for btn_info in self.action_buttons:
            widget = btn_info["widget"]
            base_text = btn_info["base_text"]
            action = btn_info["action"]

            control = active_scheme.get(action, '?')

            display_control = gamepad_name_map.get(control, control) if is_gamepad else control.upper()

            widget.configure(text=f"{base_text} ({display_control})")