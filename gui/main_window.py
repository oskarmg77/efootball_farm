# gui/main_window.py

import customtkinter as ctk
from .base_window import BaseWindow # Asumiendo que quieres usar la base para consistencia
from gui.input_test_window import InputTestWindow
from gui.vision_training_window import VisionTrainingWindow
from gui.input_monitor_window import InputMonitorWindow

class MainWindow(BaseWindow):
    """
    La ventana principal de la aplicación.
    Desde aquí se pueden lanzar otras herramientas como el simulador.
    """
    def __init__(self):
        # Usamos la clase base para unificar el estilo
        super().__init__(title="eFootball Farm - Panel Principal", width=500, height=400, resizable=False)

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        title_label = ctk.CTkLabel(main_frame, text="Asistente para eFootball", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 20))

        description_label = ctk.CTkLabel(main_frame, text="Selecciona una herramienta para comenzar:")
        description_label.pack(pady=(0, 20))

        # Botón para el simulador de acciones
        ctk.CTkButton(main_frame, text="Probar Controles (Simulador)", command=self.open_input_simulator).pack(pady=10, padx=20, fill="x")

        # Botón para el monitor de entradas en tiempo real
        ctk.CTkButton(main_frame, text="Monitorear Entradas (Real-Time)", command=self.open_input_monitor).pack(pady=10, padx=20, fill="x")

        # Botón para el entrenamiento de visión
        ctk.CTkButton(main_frame, text="Entrenar Módulo de Visión", command=self.open_vision_trainer).pack(pady=10, padx=20, fill="x")

        # Botón para cerrar la aplicación
        ctk.CTkButton(main_frame, text="Cerrar Aplicación", command=self.on_close,
                      fg_color="#D32F2F", hover_color="#B71C1C").pack(side="bottom", pady=(20, 10), padx=20)

    def open_input_simulator(self):
        """Abre la ventana de simulación de acciones."""
        win = InputTestWindow()
        win.grab_set()

    def open_input_monitor(self):
        """Abre la ventana de monitoreo de entradas en tiempo real."""
        win = InputMonitorWindow()
        win.grab_set()

    def open_vision_trainer(self):
        """Crea y muestra la ventana de entrenamiento del módulo de visión."""
        # Nota: VisionTrainingWindow usa tkinter estándar, se verá diferente.
        win = VisionTrainingWindow(self)
        win.grab_set()

    def on_close(self):
        """Cierra la aplicación."""
        self.destroy()