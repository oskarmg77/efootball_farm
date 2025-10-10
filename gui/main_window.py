import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import json

# Importa los módulos de lógica que creamos
from core.screen_capture import capture_window
from vision.gemini_analyzer import GeminiVisionAnalyzer
from config import GEMINI_API_KEY


class MainWindow(tk.Tk):
    """
    Ventana principal de la aplicación que actúa como simulador y panel de control.
    """

    def __init__(self):
        super().__init__()

        self.title("eFootball Assistant & Vision Simulator")
        self.geometry("1200x800")

        # --- Inicialización del analizador de visión ---
        # Es importante manejar el caso en que la API Key no esté disponible.
        self.analyzer = None
        if GEMINI_API_KEY:
            self.analyzer = GeminiVisionAnalyzer(api_key=GEMINI_API_KEY)
        else:
            # Manejar el error en la GUI es más amigable para el usuario.
            print("ADVERTENCIA: La API Key de Gemini no está configurada. El análisis de imagen no funcionará.")

        # --- Configuración de la interfaz ---
        self._setup_ui()

    def _setup_ui(self):
        """Crea y organiza los widgets de la interfaz."""
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Panel de Control (Izquierda) ---
        control_panel = ttk.Frame(main_frame, width=300)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        analyze_button = ttk.Button(
            control_panel,
            text="Capturar y Analizar Pantalla",
            command=self.run_analysis
        )
        analyze_button.pack(pady=10, fill=tk.X)

        # Si el analizador no se pudo crear, deshabilitamos el botón.
        if not self.analyzer:
            analyze_button.config(state=tk.DISABLED)

        # --- Panel de Resultados (Derecha) ---
        results_panel = ttk.Frame(main_frame)
        results_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Etiqueta para mostrar la captura de pantalla
        self.image_label = ttk.Label(results_panel, text="La captura de pantalla aparecerá aquí.")
        self.image_label.pack(pady=10)

        # Área de texto para mostrar el JSON resultante
        self.json_output = scrolledtext.ScrolledText(results_panel, height=15, wrap=tk.WORD)
        self.json_output.pack(pady=10, fill=tk.BOTH, expand=True)

    def run_analysis(self):
        """
        Ejecuta el ciclo completo: captura, analiza y muestra los resultados.
        """
        # 1. Capturar la ventana del juego
        screenshot = capture_window()
        if not screenshot:
            self.json_output.delete(1.0, tk.END)
            self.json_output.insert(tk.END, "Error: No se pudo capturar la ventana de eFootball.")
            return

        # 2. Mostrar la captura en la GUI
        # Redimensionamos la imagen para que quepa en la ventana
        screenshot.thumbnail((800, 450))
        photo = ImageTk.PhotoImage(screenshot)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Guardar referencia para evitar que el garbage collector la elimine

        # 3. Analizar la imagen con Gemini
        self.json_output.delete(1.0, tk.END)
        self.json_output.insert(tk.END, "Analizando imagen con Gemini, por favor espera...")
        self.update_idletasks()  # Forzar actualización de la GUI

        analysis_result = self.analyzer.analyze_image(screenshot)

        # 4. Mostrar el resultado del análisis (el JSON)
        self.json_output.delete(1.0, tk.END)
        if analysis_result:
            formatted_json = json.dumps(analysis_result, indent=2, ensure_ascii=False)
            self.json_output.insert(tk.END, formatted_json)
        else:
            self.json_output.insert(tk.END, "Error: No se pudo obtener un análisis válido de Gemini.")