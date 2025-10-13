# gui/action_simulator_window.py

import tkinter as tk
from tkinter import scrolledtext, ttk
import time

from core.input_controller import execute_action
from config import controls

class ActionSimulatorWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Simulador de Controles")
        self.geometry("800x600")

        # Variable para almacenar el esquema de control actual
        self.current_scheme = tk.StringVar(value="Teclado")

        # --- Layout Principal ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Panel de Control (Izquierda) ---
        control_panel = ttk.LabelFrame(main_frame, text="Panel de Simulación", padding="10")
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Selector de modo (Teclado/Gamepad)
        scheme_selector_frame = ttk.Frame(control_panel)
        scheme_selector_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(scheme_selector_frame, text="Modo de Control:").pack(side=tk.LEFT)
        
        keyboard_radio = ttk.Radiobutton(scheme_selector_frame, text="Teclado", variable=self.current_scheme, value="Teclado", command=self.update_button_labels)
        keyboard_radio.pack(side=tk.LEFT, padx=5)
        
        gamepad_radio = ttk.Radiobutton(scheme_selector_frame, text="Gamepad", variable=self.current_scheme, value="Gamepad", command=self.update_button_labels)
        gamepad_radio.pack(side=tk.LEFT, padx=5)

        # Botones de acción
        action_buttons_frame = ttk.Frame(control_panel)
        action_buttons_frame.pack(fill=tk.BOTH, expand=True)

        # Definimos las acciones que queremos mostrar en la GUI
        # Tupla: (Texto del botón, clave de la acción en el mapping)
        self.actions_to_show = [
            ("↑ Mover Arriba", 'MOVE_UP'),
            ("↓ Mover Abajo", 'MOVE_DOWN'),
            ("← Mover Izquierda", 'MOVE_LEFT'),
            ("→ Mover Derecha", 'MOVE_RIGHT'),
            ("Pase Corto / Presión", 'PASS_SHORT'),
            ("Disparo / Cargar", 'SHOOT'),
            ("Pase Largo / Entrada", 'PASS_HIGH'),
            ("Pase Profundo / Salir Portero", 'PASS_THROUGH'),
            ("Sprint", 'SPRINT'),
            ("Control Cercano / Cambiar Jugador", 'CHANGE_PLAYER'),
            ("Llamar 2º Defensor", 'CALL_SECOND_DEFENDER'),
            ("Confirmar", 'CONFIRM'),
            ("Atrás / Cancelar", 'BACK'),
            ("Pausa", 'PAUSE_MENU'),
        ]

        # Lista para guardar las referencias a los botones y sus claves de acción
        self.action_buttons = []

        # Crear un botón para cada acción
        for text, action_key in self.actions_to_show:
            button = ttk.Button(
                action_buttons_frame,
                text=text,
                command=lambda key=action_key: self.on_action_button_click(key)
            )
            button.pack(fill=tk.X, pady=2)
            self.action_buttons.append((button, action_key))

        # --- Panel de Registro (Derecha) ---
        log_panel = ttk.LabelFrame(main_frame, text="Registro de Acciones", padding="10")
        log_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(log_panel, wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.log_message("Simulador iniciado. Selecciona un modo y una acción.")
        self.log_message("ADVERTENCIA: Las acciones simularán pulsaciones de teclas/gamepad en la ventana activa.", "orange")

        # Actualizamos las etiquetas de los botones al estado inicial (Teclado)
        self.update_button_labels()

    def get_active_scheme(self):
        """Devuelve el diccionario de mapeo basado en la selección de la GUI."""
        if self.current_scheme.get() == "Teclado":
            return controls.KEYBOARD_MAPPING
        else:
            return controls.GAMEPAD_MAPPING

    def on_action_button_click(self, action_key: str):
        """Se ejecuta cuando se pulsa un botón de acción."""
        active_scheme = self.get_active_scheme()
        
        # Añadimos un pequeño delay para que tengas tiempo de cambiar a la ventana del juego
        self.log_message(f"Ejecutando '{action_key}' en 3 segundos...", "blue")
        self.update()
        time.sleep(3)

        # Ejecutar la acción
        result = execute_action(action_key, active_scheme)
        
        # Registrar el resultado
        if "Error" in result:
            self.log_message(result, "red")
        else:
            self.log_message(result, "green")

    def update_button_labels(self):
        """Actualiza el texto de los botones de acción según el esquema de control seleccionado."""
        active_scheme = self.get_active_scheme()
        is_gamepad = (active_scheme == controls.GAMEPAD_MAPPING)

        # Mapeo de nombres internos a nombres amigables para el usuario
        gamepad_name_map = {
            'button_south': 'A', 'button_east': 'B', 'button_west': 'X', 'button_north': 'Y',
            'left_bumper': 'LB', 'right_bumper': 'RB',
            'left_trigger': 'LT', 'right_trigger': 'RT',
            'start_button': 'Start',
            'dpad_up': '↑', 'dpad_down': '↓', 'dpad_left': '←', 'dpad_right': '→',
        }

        for (button, action_key), (base_text, _) in zip(self.action_buttons, self.actions_to_show):
            control = active_scheme.get(action_key, '?')
            
            # Formateamos el nombre del botón de gamepad para que sea más legible
            display_control = gamepad_name_map.get(control, control.upper()) if is_gamepad else control.upper()
            button.config(text=f"{base_text} ({display_control})")

    def log_message(self, message: str, color: str = "black"):
        """Añade un mensaje al registro de texto con un color específico."""
        self.log_text.config(state=tk.NORMAL)
        timestamp = time.strftime('%H:%M:%S')
        full_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, full_message)
        self.log_text.tag_add(color, f"{self.log_text.index('end-2c')} linestart", f"{self.log_text.index('end-2c')} lineend")
        self.log_text.tag_config(color, foreground=color)
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END) # Auto-scroll