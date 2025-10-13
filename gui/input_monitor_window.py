# gui/input_monitor_window.py

import customtkinter as ctk
import threading
from queue import Queue

from .base_window import BaseWindow
from pynput import keyboard
try:
    from inputs import get_gamepad, UnpluggedError
except ImportError:
    get_gamepad = None

from config.controls import KEYBOARD_MAPPING, GAMEPAD_MAPPING

class InputMonitorWindow(BaseWindow):
    """
    Una ventana para monitorear en tiempo real las entradas de teclado y gamepad
    y verificar si están correctamente mapeadas en controls.py.
    """
    def __init__(self):
        super().__init__(title="Monitor de Entradas", width=600, height=400)

        # --- Estado y Lógica ---
        self.key_to_action_map = {v: k for k, v in KEYBOARD_MAPPING.items()}
        self.gamepad_to_action_map = {v: k for k, v in GAMEPAD_MAPPING.items()}

        self.stop_event = threading.Event()
        self.queue = Queue()
        self.keyboard_listener = None # Referencia para el listener

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- Construcción de la GUI ---
        self._create_widgets()

        # --- Iniciar listeners ---
        self.start_listeners()
        self.process_queue()

    def _create_widgets(self):
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        main_frame.grid_columnconfigure(1, weight=1)

        # --- Sección de Teclado ---
        kb_frame = ctk.CTkFrame(main_frame)
        kb_frame.pack(fill="x", pady=(0, 15), padx=10)
        kb_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(kb_frame, text="Última Tecla Pulsada:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.last_key_label = ctk.CTkLabel(kb_frame, text="---", font=ctk.CTkFont(weight="bold"))
        self.last_key_label.grid(row=0, column=1, sticky="w", padx=10)

        ctk.CTkLabel(kb_frame, text="Acción Mapeada:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.key_action_label = ctk.CTkLabel(kb_frame, text="---")
        self.key_action_label.grid(row=1, column=1, sticky="w", padx=10)

        # --- Sección de Gamepad ---
        gp_frame = ctk.CTkFrame(main_frame)
        gp_frame.pack(fill="x", padx=10)
        gp_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(gp_frame, text="Último Botón Pulsado:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.last_gamepad_label = ctk.CTkLabel(gp_frame, text="---", font=ctk.CTkFont(weight="bold"))
        self.last_gamepad_label.grid(row=0, column=1, sticky="w", padx=10)

        ctk.CTkLabel(gp_frame, text="Acción Mapeada:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.gamepad_action_label = ctk.CTkLabel(gp_frame, text="---")
        self.gamepad_action_label.grid(row=1, column=1, sticky="w", padx=10)

        if not get_gamepad:
            self.last_gamepad_label.configure(text="Librería 'inputs' no encontrada.", text_color="orange")

        ctk.CTkButton(main_frame, text="Cerrar", command=self.on_close).pack(side="bottom", pady=(20, 0))

    def start_listeners(self):
        threading.Thread(target=self._keyboard_listener, daemon=True).start()
        if get_gamepad:
            threading.Thread(target=self._gamepad_listener, daemon=True).start()

    def _keyboard_listener(self):
        # Guardamos la instancia del listener para poder detenerla después
        self.keyboard_listener = keyboard.Listener(on_press=self._on_key_press)
        self.keyboard_listener.start()
        self.keyboard_listener.join()

    def _on_key_press(self, key):
        if self.stop_event.is_set(): return False
        key_str = key.char if hasattr(key, 'char') and key.char is not None else key.name
        self.queue.put(("keyboard", key_str))
        return True

    def _gamepad_listener(self):
        try:
            while not self.stop_event.is_set():
                for event in get_gamepad():
                    if event.ev_type == 'Key' and event.state == 1:
                        self.queue.put(("gamepad", event.code))
        except (OSError, IOError, UnpluggedError): # Capturamos también el error de desconexión
            self.queue.put(("gamepad_error", "No se detecta ningún gamepad."))

    def process_queue(self):
        try:
            source, data = self.queue.get_nowait()
            if source == "keyboard":
                self.last_key_label.configure(text=data)
                action = self.key_to_action_map.get(data)
                if action:
                    self.key_action_label.configure(text=f"✅ {action}", text_color="green")
                else:
                    self.key_action_label.configure(text="❌ No Mapeada", text_color="red")
            
            elif source == "gamepad":
                self.last_gamepad_label.configure(text=data)
                action = self.gamepad_to_action_map.get(data)
                if action:
                    self.gamepad_action_label.configure(text=f"✅ {action}", text_color="green")
                else:
                    self.gamepad_action_label.configure(text="❌ No Mapeada", text_color="red")
            
            elif source == "gamepad_error":
                self.last_gamepad_label.configure(text=data, text_color="orange")

        except Exception:
            pass
        
        self.after(50, self.process_queue)

    def on_close(self):
        self.stop_event.set()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.destroy()