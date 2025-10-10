# gui/main_window.py

import tkinter as tk
from tkinter import ttk
from gui.action_simulator_window import ActionSimulatorWindow
from gui.vision_training_window import VisionTrainingWindow

class MainWindow(tk.Tk):
    """
    La ventana principal de la aplicación.
    Desde aquí se pueden lanzar otras herramientas como el simulador.
    """
    def __init__(self):
        super().__init__()

        self.title("eFootball Farm - Panel Principal")
        self.geometry("500x300")

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Asistente para eFootball", font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(0, 20))

        description_label = ttk.Label(main_frame, text="Selecciona una herramienta para comenzar.")
        description_label.pack(pady=(0, 25))

        simulator_button = ttk.Button(main_frame, text="Abrir Simulador de Controles", command=self.open_simulator)
        simulator_button.pack(pady=10, ipadx=10, ipady=5)

        vision_button = ttk.Button(main_frame, text="Módulo de Visión / Entrenamiento", command=self.open_vision_trainer)
        vision_button.pack(pady=10, ipadx=10, ipady=5)

    def open_simulator(self):
        """Crea y muestra la ventana del simulador de acciones."""
        simulator_win = ActionSimulatorWindow(self)
        simulator_win.grab_set() # Hace que la ventana del simulador sea modal

    def open_vision_trainer(self):
        """Crea y muestra la ventana de entrenamiento del módulo de visión."""
        training_win = VisionTrainingWindow(self)
        training_win.grab_set()