# eFootball Farm - Agente IA con Gemini

Un bot inteligente diseñado para automatizar tareas repetitivas en el videojuego eFootball, utilizando la API de Google Gemini para el reconocimiento visual de menús y la toma de decisiones.

---

## 📜 Tabla de Contenidos

- [Sobre el Proyecto](#-sobre-el-proyecto)
- [Estado Actual](#-estado-actual-del-proyecto)
- [Características](#-características)
- [Estructura de Archivos](#-estructura-de-archivos)
- [Cómo Empezar](#-cómo-empezar-instalación)
- [Uso](#-uso)
- [Roadmap](#-roadmap-planes-a-futuro)
- [Licencia](#-licencia)

---

## 📖 Sobre el Proyecto

El objetivo de este proyecto es crear un agente autónomo capaz de navegar por los menús del juego eFootball para realizar acciones específicas solicitadas por el usuario. En lugar de depender de coordenadas de píxeles frágiles o reconocimiento de imágenes basado en plantillas, este bot utiliza un modelo de lenguaje multimodal (Google Gemini) para "ver" y "entender" la pantalla del juego.

El usuario podrá dar una orden de alto nivel, como *"Jugar el evento de la IA llamado 'Nationals'"*, y el bot se encargará de realizar todos los pasos necesarios para cumplir el objetivo.

**Tecnologías Clave:**
*   **Lenguaje:** Python 3
*   **Visión IA:** Google Gemini API
*   **Interfaz Gráfica:** CustomTkinter
*   **Control de Input:** `pynput` (Teclado) y `inputs` (Gamepad)

---

## ✨ Estado Actual del Proyecto

El proyecto cuenta con una base sólida y funcional, con varias herramientas GUI que facilitan el desarrollo y la depuración.

*   **Estructura de Proyecto Modular:** El código está organizado en módulos con responsabilidades claras (`core`, `config`, `gui`, `vision`, `utils`), facilitando la escalabilidad y el mantenimiento.

*   **Interfaz Gráfica Robusta:**
    *   Panel de control principal para lanzar las distintas herramientas.
    *   Gestión de ventanas mejorada para evitar errores y asegurar que las ventanas secundarias aparezcan correctamente.
    *   Clases base (`BaseWindow`, `BaseToplevelWindow`) para un estilo y comportamiento consistentes.

*   **Sistema de Logging Centralizado:**
    *   Se ha implementado un módulo `utils/logger.py` que configura un logger para toda la aplicación.
    *   Los logs se guardan en `logs/app.log` y se muestran en la consola, facilitando la depuración.

*   **Herramientas de Depuración Funcionales:**
    *   **Simulador de Controles:** Una ventana para probar la ejecución de acciones de juego (`disparo`, `pase`, etc.) tanto con teclado como con gamepad.
    *   **Monitor de Entradas:** Una herramienta para ver en tiempo real qué tecla o botón se está pulsando y a qué acción del juego corresponde, ideal para configurar los controles.
    *   **Entrenador del Módulo de Visión:** Una GUI asistida para mapear las pantallas del juego, capturando la acción del usuario que lleva de una pantalla a otra.

---

## 🚀 Características

*   **Panel de Control Central:** Una GUI principal para acceder a todas las funcionalidades.
*   **Simulador de Acciones:** Permite probar la ejecución de acciones del juego en un entorno controlado.
*   **Monitor de Entradas en Tiempo Real:** Facilita la configuración y depuración de los controles de teclado y gamepad.
*   **Asistente de Entrenamiento de Visión:** Una herramienta guiada para construir el mapa de navegación que usará la IA.
*   **Control Dual (Teclado/Gamepad):** Soporte para simular entradas de ambos dispositivos.
*   **Logging Detallado:** Registro de todos los eventos importantes de la aplicación para una fácil depuración.

---

## 📂 Estructura de Archivos

```bash
/efootball_farm/
│
├── main.py                     # Punto de entrada que lanza la GUI.
├── requirements.txt            # Dependencias del proyecto.
├── README.md                   # Este archivo.
├── .gitignore                  # Archivos ignorados por Git.
│
├── config/
│   ├── controls.py             # Mapeo de acciones a teclas/botones (ej. 'SHOOT': 'x').
│   └── settings.py             # Configuraciones generales (API keys, etc.).
│
├── core/
│   ├── input_controller.py     # Lógica para simular pulsaciones de teclado y gamepad.
│   ├── screen_capture.py     # Funciones para tomar capturas de pantalla.
│   └── game_manager.py         # (Futuro) Lógica de alto nivel para gestionar el juego.
│
├── gui/
│   ├── base_window.py          # Clases base para las ventanas (principal y secundarias).
│   ├── main_window.py          # Ventana principal de la aplicación.
│   ├── input_test_window.py    # GUI para el simulador de controles.
│   ├── input_monitor_window.py # GUI para el monitor de entradas.
│   └── vision_training_window.py # GUI para el entrenamiento del módulo de visión.
│
├── vision/
│   ├── action_monitor.py       # Captura las acciones del usuario durante el entrenamiento.
│   └── gemini_analyzer.py      # (Futuro) Envía capturas a Gemini y analiza la respuesta.
│
├── utils/
│   └── logger.py               # Configuración del logger centralizado.
│
├── logs/
│   └── app.log                 # Archivo de log donde se guarda la actividad.
│
├── prompts/
│   └── identify_menu_prompt.txt # Prompt para que Gemini analice las capturas de pantalla.
│
└── ... (otros directorios como .venv, .idea, etc.)
```

---

## 🚀 Cómo Empezar (Instalación)

Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

### Prerrequisitos

1.  **Python:** Asegúrate de tener instalado Python 3.8 o superior.
2.  **Git:** Necesario para clonar el repositorio.

### Pasos de Instalación

1.  **Clona el repositorio:**
    ```sh
    git clone https://github.com/tu_usuario/efootball-farm.git
    cd efootball-farm
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```sh
    python -m venv .venv
    ```
    *   En Windows, actívalo con: `.\.venv\Scripts\activate`
    *   En macOS/Linux, actívalo con: `source .venv/bin/activate`

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

Esto abrirá la ventana principal. Desde allí, puedes:
*   **Probar Controles:** Abrir el simulador para enviar comandos al juego.
*   **Monitorear Entradas:** Verificar qué teclas/botones se están detectando.
*   **Entrenar Módulo de Visión:** Iniciar el proceso de mapeo de pantallas del juego.

---

## 🔮 Roadmap (Planes a Futuro)

1.  **Integración Completa de Gemini:**
    *   Implementar la lógica en `vision/gemini_analyzer.py` para enviar capturas de pantalla a la API de Gemini.
    *   Desarrollar un sistema para parsear la respuesta de Gemini (JSON) y extraer el menú actual y las opciones disponibles.

2.  **Desarrollo del Agente IA (`agent`):**
    *   **Gestor de Estado (`GameState`):** Una clase que mantenga la "memoria" del bot (menú actual, objetivo, etc.).
    *   **Planificador de Acciones (`ActionPlanner`):** El cerebro que decidirá la siguiente acción a tomar para alcanzar el objetivo.
    *   **Motor de Ejecución:** Un bucle principal que conecte la visión, el planificador y el controlador de input.

3.  **Mejoras en la GUI:**
    *   Añadir una pestaña o sección en la ventana principal para dar órdenes al bot.
    *   Mostrar el estado y los logs del agente en tiempo real en la interfaz.

---

## 📄 Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.
