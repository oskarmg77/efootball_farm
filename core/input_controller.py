# core/input_controller.py

import pydirectinput
import vgamepad as vg
import time

# Importamos todas las variables de control necesarias
from config.controls import (
    ACTIVE_CONTROL_SCHEME,
    KEYBOARD_MAPPING,
    GAMEPAD_MAPPING
)

# --- INICIALIZACIÓN DEL GAMEPAD VIRTUAL ---
# Se intenta crear un gamepad virtual al iniciar el programa.
# Solo se usará si ACTIVE_CONTROL_SCHEME está configurado para gamepad.
try:
    gamepad = vg.VX360Gamepad()
    print("Controlador de Gamepad: Gamepad virtual (VBus) inicializado correctamente.")
except Exception:
    gamepad = None
    print("ADVERTENCIA: No se pudo inicializar el gamepad virtual. Asegúrate de que ViGEmBus está instalado.")
    print("El control por gamepad no funcionará.")

# Diccionario para traducir nuestros nombres de botones de gamepad a los códigos de la librería vgamepad
# --- ESTA ES LA SECCIÓN CORREGIDA ---
VGPAD_BUTTON_CODES = {
    'dpad_up': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    'dpad_down': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    'dpad_left': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    'dpad_right': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    'button_south': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    'button_east': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
}

def execute_action(action: str) -> str:
    """
    Recibe una acción abstracta (ej. 'UP'), comprueba el esquema de control
    activo (teclado o gamepad) y ejecuta la pulsación correspondiente.

    Devuelve un string con el resultado de la operación.
    """
    # 1. Obtiene el control específico (ej. 'w' o 'dpad_up') desde el esquema activo
    control_to_press = ACTIVE_CONTROL_SCHEME.get(action)

    if not control_to_press:
        return f"Error: Acción '{action}' no definida en el esquema de control activo."

    # 2. Comprueba qué esquema está activo y actúa en consecuencia
    if ACTIVE_CONTROL_SCHEME is KEYBOARD_MAPPING:
        # MODO TECLADO
        try:
            pydirectinput.press(control_to_press)
            return f"Acción '{action}' ejecutada -> Tecla '{control_to_press}'"
        except Exception as e:
            return f"Error de teclado al pulsar '{control_to_press}': {e}"

    elif ACTIVE_CONTROL_SCHEME is GAMEPAD_MAPPING:
        # MODO GAMEPAD
        if not gamepad:
            return "Error: Se intentó usar el gamepad, pero no está inicializado."

        # Busca el código del botón en nuestro diccionario de traducción
        button_code = VGPAD_BUTTON_CODES.get(control_to_press)
        if not button_code:
            return f"Error: El control de gamepad '{control_to_press}' no tiene un código de botón asociado."

        try:
            gamepad.press_button(button=button_code)
            gamepad.update()
            time.sleep(0.1)  # Pausa breve para asegurar que el juego registre la pulsación
            gamepad.release_button(button=button_code)
            gamepad.update()
            return f"Acción '{action}' ejecutada -> Botón de Gamepad '{control_to_press}'"
        except Exception as e:
            return f"Error de gamepad al pulsar '{control_to_press}': {e}"

    else:
        return "Error: Esquema de control no reconocido."