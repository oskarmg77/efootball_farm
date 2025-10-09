# La ventana de prueba para el gamepad/teclado.
# gui/input_test_window.py

import customtkinter as ctk
from .base_window import BaseWindow
from core.input_controller import execute_action  # ¡Importante! Conectamos con la lógica del bot
from config.controls import (ACTION_UP, ACTION_DOWN, ACTION_LEFT,
                             ACTION_RIGHT, ACTION_ACCEPT, ACTION_CANCEL)


class InputTestWindow(BaseWindow):
    def __init__(self):
        # Llamamos al constructor de la clase base con sus parámetros
        super().__init__(title="Prueba de Controles", width=350, height=450)

        # --- Frame Principal ---
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # --- Lógica de los botones ---
        def on_button_click(action: str):
            """Llama a la lógica del controlador y muestra el resultado."""
            message = execute_action(action)
            # Por ahora lo mostramos en la consola.
            # En el futuro, se podría mostrar en una etiqueta de estado en la GUI.
            print(message)

        # --- Título ---
        title_label = ctk.CTkLabel(main_frame, text="Simulador de Acciones", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=12, padx=10)

        # --- Botones de Dirección (DPad) ---
        dpad_frame = ctk.CTkFrame(main_frame)
        dpad_frame.pack(pady=10)

        # Usamos grid para colocar los botones como una cruceta
        btn_up = ctk.CTkButton(dpad_frame, text="▲", width=50, command=lambda: on_button_click(ACTION_UP))
        btn_up.grid(row=0, column=1, padx=5, pady=5)

        btn_left = ctk.CTkButton(dpad_frame, text="◀", width=50, command=lambda: on_button_click(ACTION_LEFT))
        btn_left.grid(row=1, column=0, padx=5, pady=5)

        btn_right = ctk.CTkButton(dpad_frame, text="▶", width=50, command=lambda: on_button_click(ACTION_RIGHT))
        btn_right.grid(row=1, column=2, padx=5, pady=5)

        btn_down = ctk.CTkButton(dpad_frame, text="▼", width=50, command=lambda: on_button_click(ACTION_DOWN))
        btn_down.grid(row=2, column=1, padx=5, pady=5)

        # --- Botones de Acción ---
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(pady=20)

        btn_accept = ctk.CTkButton(action_frame, text="Aceptar", fg_color="green", hover_color="#006400", # DarkGreen
                                   command=lambda: on_button_click(ACTION_ACCEPT))
        btn_accept.pack(side="left", padx=10)

        btn_cancel = ctk.CTkButton(action_frame, text="Cancelar", fg_color="red", hover_color="#8B0000", # DarkRed
                                   command=lambda: on_button_click(ACTION_CANCEL))
        btn_cancel.pack(side="left", padx=10)