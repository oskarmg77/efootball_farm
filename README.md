# eFootball Automator - Agente IA con Gemini

Un bot inteligente diseñado para automatizar tareas repetitivas en el videojuego eFootball, utilizando la API de Google Gemini para el reconocimiento visual de menús y la toma de decisiones.

---

## 📜 Sobre el Proyecto

El objetivo de este proyecto es crear un agente autónomo capaz de navegar por los menús del juego eFootball para realizar acciones específicas solicitadas por el usuario. En lugar de depender de coordenadas de píxeles frágiles o reconocimiento de imágenes basado en plantillas, este bot utiliza un modelo de lenguaje multimodal (Google Gemini) para "ver" y "entender" la pantalla del juego.

El usuario podrá dar una orden de alto nivel, como *"Jugar el evento de la IA llamado 'Nationals'"*, y el bot se encargará de realizar todos los pasos necesarios para cumplir el objetivo: navegar al menú de eventos, encontrar el evento correcto, iniciar el partido y, potencialmente, jugarlo.

**Tecnologías Clave:**
*   **Lenguaje:** Python 3
*   **Visión IA:** Google Gemini API
*   **Interfaz Gráfica:** CustomTkinter
*   **Control de Input:** Pydirectinput (Teclado) y VGamepad/ViGEmBus (Gamepad Virtual)

---

## ✨ Estado Actual del Proyecto (Lo que ya tenemos)

Actualmente, se ha construido la base fundamental del proyecto, enfocada en la modularidad, las herramientas de control y el inicio del módulo de visión.

*   **Estructura de Proyecto Sólida:** El código está organizado en módulos con responsabilidades claras (`core`, `config`, `gui`, `vision`), facilitando la escalabilidad y el mantenimiento.

*   **Interfaz Gráfica Mejorada:**
    *   Una ventana principal que actúa como panel de control, con un nuevo botón para cerrar la aplicación.
    *   Una ventana de depuración para probar el sistema de control de input en tiempo real.
    *   Se ha mejorado la consistencia de la interfaz, permitiendo controlar si las ventanas son redimensionables o no.
    *   Apariencia moderna y unificada gracias a la librería CustomTkinter.

*   **Herramienta de Entrenamiento para el Módulo de Visión:**
    *   Se ha creado una nueva ventana (`VisionTrainingWindow`) para guiar al usuario en el proceso de mapeo de las pantallas del juego.
    *   **Interfaz Intuitiva:** La ventana utiliza un panel de instrucciones dinámico que cambia de color y texto para indicar al usuario exactamente qué hacer en cada paso (ej. "Ve a la pantalla X", "Realiza una acción en el juego", "Analiza la nueva pantalla").
    *   **Captura de Acciones:** El sistema ahora puede "escuchar" y registrar la acción (teclado o gamepad) que el usuario realiza para navegar entre dos menús.
    *   Esto sienta las bases para construir el mapa de navegación que el agente de IA usará para moverse por el juego.

*   **Controlador de Input Flexible:**
    *   Capacidad para simular pulsaciones tanto de **teclado** como de **gamepad**.
    *   El cambio entre teclado y gamepad se realiza fácilmente modificando una sola variable en un archivo de configuración (`config/controls.py`).

*   **Herramienta de Prueba de Controles:** La GUI incluye una interfaz específica para enviar comandos de movimiento (`arriba`, `abajo`, `aceptar`, etc.) y verificar que el sistema operativo y el juego los reciben correctamente.

---

## 📂 Estructura de Archivos

```bash
/efootball-automator/
│
├── main.py                     # Punto de entrada que lanza la GUI.
│
├── config/
│   ├── settings.py             # Configuraciones (API keys, etc.).
│   └── controls.py             # Mapeo de acciones a teclas/botones.
│
├── core/
│   ├── input_controller.py     # Lógica para simular pulsaciones (teclado/gamepad).
│   └── ...
│
├── gui/
│   ├── base_window.py          # Clase base para todas las ventanas.
│   ├── main_window.py          # GUI principal de la aplicación.
│   ├── input_test_window.py    # GUI para probar los controles.
│   └── vision_training_window.py # GUI para el entrenamiento del módulo de visión.
│
├── vision/
│   └── action_monitor.py       # Captura las acciones del usuario (teclado/gamepad).
│
├── agent/                      # (Aún por desarrollar) El cerebro del bot.
│
├── requirements.txt            # Dependencias del proyecto.
└── README.md                   # Este archivo.
```

---

## 🚀 Cómo Empezar (Instalación)

Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

### Prerrequisitos

1.  **Python:** Asegúrate de tener instalado Python 3.8 o superior.
2.  **Git:** Necesario para clonar el repositorio.
3.  **Driver ViGEmBus (Opcional pero recomendado):** Para que la simulación de gamepad funcione, es **imprescindible** instalar este driver en tu sistema Windows.
    *   [Descargar la última versión de ViGEmBus](https://github.com/ViGEm/ViGEmBus/releases)

### Pasos de Instalación

1.  **Clona el repositorio:**
    ```sh
    git clone https://github.com/tu_usuario/efootball-automator.git
    cd efootball-automator
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```sh
    python -m venv venv
    ```
    *   En Windows, actívalo con: `.\venv\Scripts\activate`
    *   En macOS/Linux, actívalo con: `source venv/bin/activate`

3.  **Instala las dependencias:**
    ```sh
    pip install -r requirements.txt
    ```

---

## 🛠️ Uso

Una vez completada la instalación, simplemente ejecuta el archivo `main.py`:

```sh
python main.py
```

Esto abrirá la ventana principal de la aplicación. Desde allí, puedes usar el botón "Probar Controles" para verificar que la simulación de input funciona correctamente.

---

## 🔮 Roadmap (Planes a Futuro)

Esta base es solo el comienzo. Los siguientes grandes pasos son:

1.  **Módulo de Visión - Integración con Gemini:**
    *   Implementar una función en `screen_capture.py` para tomar capturas de la ventana de eFootball.
    *   Crear el módulo `vision/gemini_analyzer.py` que enviará estas capturas a la API de Gemini con un prompt específico para identificar el menú actual y las opciones seleccionables.
    *   Desarrollar un sistema para parsear la respuesta (probablemente JSON) de Gemini a un formato estructurado.

2.  **Gestor de Estado (`GameState`):**
    *   Crear una clase que actúe como la "memoria" del bot, almacenando la información recibida de Gemini (ej: `current_menu`, `available_options`, `selected_option`).

3.  **Desarrollo del Agente (El Cerebro):**
    *   **Planificador de Acciones (`ActionPlanner`):** El componente más inteligente. Recibirá un objetivo del usuario y, basándose en el estado actual del juego, generará una secuencia de acciones (ej: `['DOWN', 'DOWN', 'ACCEPT']`).
    *   **Navegador (`Navigator`):** Ejecutará el plan generado por el planificador, llamando a `input_controller` para cada paso.

4.  **Integración Completa en la GUI:**
    *   Conectar los botones "Iniciar Bot" y "Detener Bot" para que inicien y detengan el bucle principal del agente (en un hilo separado para no congelar la GUI).
    *   Mostrar los logs y el estado del bot en tiempo real en el panel derecho de la ventana principal.

---

## 📄 Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.
