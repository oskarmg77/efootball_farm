# vision/action_monitor.py

import threading
from pynput import keyboard
try:
    from inputs import get_gamepad
except ImportError:
    get_gamepad = None


class ActionMonitor:
    """
    Escucha las entradas del teclado y/o gamepad en hilos separados para no bloquear la GUI.
    Traduce las entradas a acciones abstractas del juego (ej. 'MOVE_UP', 'CONFIRM').
    """

    def __init__(self, keyboard_mapping, gamepad_mapping):
        """
        Inicializa el monitor de acciones.

        Args:
            keyboard_mapping (dict): Mapeo de acciones a teclas de teclado.
            gamepad_mapping (dict): Mapeo de acciones a botones de gamepad.
        """
        # Invertimos los mapeos para una búsqueda rápida: {'up': 'MOVE_UP', ...}
        self.key_to_action_map = {v: k for k, v in keyboard_mapping.items()}
        self.gamepad_to_action_map = {v: k for k, v in gamepad_mapping.items()}

        self.keyboard_listener_thread = None
        self.gamepad_listener_thread = None

        self.last_action = None
        self.lock = threading.Lock()
        self.stop_event = threading.Event()

        if not get_gamepad:
            print("ADVERTENCIA: La librería 'inputs' no está instalada. El gamepad no funcionará. Instálala con: pip install inputs")

    def _on_key_press(self, key):
        """
        Callback para el listener del teclado. Se ejecuta al presionar una tecla.
        """
        try:
            key_str = key.char
        except AttributeError:
            key_str = key.name

        if key_str in self.key_to_action_map:
            action = self.key_to_action_map[key_str]
            with self.lock:
                self.last_action = action
            self.stop_event.set() # Señaliza que se ha capturado una acción
            return False # Detiene el listener de teclado

    def _run_keyboard_listener(self):
        """Función que se ejecuta en un hilo para escuchar el teclado."""
        # pynput.keyboard.Listener es bloqueante, pero se detendrá cuando _on_key_press devuelva False
        with keyboard.Listener(on_press=self._on_key_press) as listener:
            # El listener se une (espera) aquí. Si el stop_event se activa desde otro hilo,
            # el listener se detendrá explícitamente.
            self.stop_event.wait()
            listener.stop()

    def _run_gamepad_listener(self):
        """Función que se ejecuta en un hilo para escuchar el gamepad."""
        if not get_gamepad:
            return # No hacer nada si la librería no está disponible

        try:
            while not self.stop_event.is_set():
                events = get_gamepad()
                for event in events:
                    # Nos interesan solo las pulsaciones de botones (estado 1)
                    if event.ev_type == 'Key' and event.state == 1:
                        if event.code in self.gamepad_to_action_map:
                            action = self.gamepad_to_action_map[event.code]
                            with self.lock:
                                self.last_action = action
                            self.stop_event.set() # Señaliza y sale del bucle
                            return
        except Exception as e:
            # Puede fallar si no hay un gamepad conectado
            if "No gamepad found" not in str(e):
                print(f"Error en el listener del gamepad: {e}")

    def listen_for_single_action(self):
        """
        Inicia listeners para teclado y gamepad. Se detienen tras capturar la primera acción.
        Esta función no es bloqueante.
        """
        self.stop() # Asegurarse de que no hay listeners antiguos corriendo

        with self.lock:
            self.last_action = None
        self.stop_event.clear()

        # Iniciar listener de teclado
        self.keyboard_listener_thread = threading.Thread(target=self._run_keyboard_listener, daemon=True)
        self.keyboard_listener_thread.start()

        # Iniciar listener de gamepad si es posible
        if get_gamepad:
            self.gamepad_listener_thread = threading.Thread(target=self._run_gamepad_listener, daemon=True)
            self.gamepad_listener_thread.start()

    def get_captured_action(self):
        """
        Devuelve la última acción capturada y la resetea.
        Es seguro para usar desde diferentes hilos gracias al Lock.

        Returns: str or None
        """
        with self.lock:
            action = self.last_action
            self.last_action = None
            return action

    def stop(self):
        """
        Detiene todos los listeners activos de forma segura.
        """
        self.stop_event.set() # Señaliza a los hilos que deben parar

        # Esperar a que los hilos terminen
        if self.keyboard_listener_thread and self.keyboard_listener_thread.is_alive():
            # El listener de pynput necesita un pequeño truco para despertarlo si está esperando
            try:
                controller = keyboard.Controller()
                controller.press(keyboard.Key.esc)
                controller.release(keyboard.Key.esc)
            except Exception:
                pass # No importa si falla
            self.keyboard_listener_thread.join(timeout=0.5)

        if self.gamepad_listener_thread and self.gamepad_listener_thread.is_alive():
            self.gamepad_listener_thread.join(timeout=0.5)