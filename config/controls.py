# config/controls.py

# --- Acciones Abstractas del Menú ---
# Estas son las acciones que tu agente entiende.
# Usamos cadenas de texto para que sea fácil leer los logs.
ACTION_UP = 'UP'
ACTION_DOWN = 'DOWN'
ACTION_LEFT = 'LEFT'
ACTION_RIGHT = 'RIGHT'
ACTION_ACCEPT = 'ACCEPT' # Aceptar, Confirmar, Entrar
ACTION_CANCEL = 'CANCEL' # Cancelar, Atrás

# --- Mapeo a Teclado ---
# Aquí traduces las acciones abstractas a teclas específicas.
# Si cambias los controles en el juego, solo tienes que editar este diccionario.
KEYBOARD_MAPPING = {
    ACTION_UP: 'w',
    ACTION_DOWN: 's',
    ACTION_LEFT: 'a',
    ACTION_RIGHT: 'd',
    ACTION_ACCEPT: 'enter',
    ACTION_CANCEL: 'esc',
}

# --- Mapeo a Gamepad ---
# Nombres de botones abstractos que usará el controlador del gamepad.
GAMEPAD_MAPPING = {
    ACTION_UP: 'dpad_up',
    ACTION_DOWN: 'dpad_down',
    ACTION_LEFT: 'dpad_left',
    ACTION_RIGHT: 'dpad_right',
    ACTION_ACCEPT: 'button_south',  # Botón A en Xbox, X en PlayStation
    ACTION_CANCEL: 'button_east',   # Botón B en Xbox, Círculo en PlayStation
}

# --- Selección del Dispositivo ---
# ¡ESTE ES EL INTERRUPTOR PRINCIPAL!
# Cambia esta variable para que el bot use teclado o gamepad.
# El resto del código se adaptará automáticamente.
ACTIVE_CONTROL_SCHEME = KEYBOARD_MAPPING
# Para usar el gamepad, comenta la línea de arriba y descomenta la de abajo:
# ACTIVE_CONTROL_SCHEME = GAMEPAD_MAPPING