# gui/main_window.py
import customtkinter as ctk
from .base_window import BaseWindow
from gui.input_test_window import InputTestWindow
from gui.vision_training_window import VisionTrainingWindow
from gui.input_monitor_window import InputMonitorWindow
from utils.logger import log

class MainWindow(BaseWindow):
    """
    La ventana principal de la aplicación.
    Desde aquí se pueden lanzar otras herramientas como el simulador.
    """
    def __init__(self):
        super().__init__(title="eFootball Farm - Panel Principal", width=500, height=400, resizable=False)

        # Atributos para almacenar las ventanas secundarias y evitar que se abran duplicados
        self.win_input_test = None
        self.win_input_monitor = None
        self.win_vision_trainer = None

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        title_label = ctk.CTkLabel(main_frame, text="Asistente para eFootball", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 20))

        description_label = ctk.CTkLabel(main_frame, text="Selecciona una herramienta para comenzar:")
        description_label.pack(pady=(0, 20))

        ctk.CTkButton(main_frame, text="Probar Controles (Simulador)", command=self.open_input_simulator).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(main_frame, text="Monitorear Entradas (Real-Time)", command=self.open_input_monitor).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(main_frame, text="Entrenar Módulo de Visión", command=self.open_vision_trainer).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(main_frame, text="Cerrar Aplicación", command=self.on_close,
                      fg_color="#D32F2F", hover_color="#B71C1C").pack(side="bottom", pady=(20, 10), padx=20)
        
        # Asegurarse de que al cerrar la ventana principal se llame a on_close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _open_window(self, window_class, attribute_name, *args):
        """Función genérica para abrir ventanas secundarias, evitando duplicados."""
        # Comprobar si la ventana ya existe y está visible
        window_instance = getattr(self, attribute_name)
        if window_instance and window_instance.winfo_exists():
            log.warning(f"La ventana {window_class.__name__} ya está abierta.")
            window_instance.focus_set()  # Poner el foco en la ventana existente
            return

        log.info(f"Abriendo la ventana {window_class.__name__}.")
        new_window = window_class(*args)
        setattr(self, attribute_name, new_window) # Guardar la referencia
        
        new_window.transient(self) # Hacer que la ventana aparezca delante de la principal
        new_window.focus_set()     # Darle el foco a la nueva ventana

    def open_input_simulator(self):
        """Abre la ventana de simulación de acciones."""
        log.info("Botón 'Probar Controles (Simulador)' presionado.")
        self._open_window(InputTestWindow, "win_input_test")

    def open_input_monitor(self):
        """Abre la ventana de monitoreo de entradas en tiempo real."""
        log.info("Botón 'Monitorear Entradas (Real-Time)' presionado.")
        self._open_window(InputMonitorWindow, "win_input_monitor")

    def open_vision_trainer(self):
        """Crea y muestra la ventana de entrenamiento del módulo de visión."""
        log.info("Botón 'Entrenar Módulo de Visión' presionado.")
        self._open_window(VisionTrainingWindow, "win_vision_trainer", self)

    def on_close(self):
        """Cierra la aplicación de forma segura."""
        log.info("Cerrando la aplicación...")
        self.quit() # Termina el mainloop de forma segura
        self.destroy() # Destruye la ventana principal
