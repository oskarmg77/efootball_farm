# config/controls.py

"""
Este archivo centraliza todos los mapeos de control para el juego.
Define las acciones abstractas y las asigna a teclas de teclado o botones de gamepad.
"""

# --- ACCIONES ABSTRACTAS DEL JUEGO ---
# Usamos nombres descriptivos para cada acción posible.
# Estas constantes se usarán en toda la aplicación para evitar errores de tipeo.

# Movimiento
MOVE_UP = 'MOVE_UP'
MOVE_DOWN = 'MOVE_DOWN'
MOVE_LEFT = 'MOVE_LEFT'
MOVE_RIGHT = 'MOVE_RIGHT'

# Acciones de Menú
CONFIRM = 'CONFIRM'
BACK = 'BACK'
PAUSE_MENU = 'PAUSE_MENU'

# Acciones en Juego
SPRINT = 'SPRINT'
PASS_SHORT = 'PASS_SHORT'
PASS_HIGH = 'PASS_HIGH'
PASS_THROUGH = 'PASS_THROUGH'
SHOOT = 'SHOOT'
CHANGE_PLAYER = 'CHANGE_PLAYER'
CALL_SECOND_DEFENDER = 'CALL_SECOND_DEFENDER'


KEYBOARD_MAPPING = {
    # Movimiento y Navegación en Menús
    MOVE_UP: 'up',
    MOVE_DOWN: 'down',
    MOVE_LEFT: 'left',
    MOVE_RIGHT: 'right',

    # Acciones en el Juego (Ataque)
    SPRINT: 'c',
    PASS_SHORT: 'x',
    PASS_HIGH: 'd',
    PASS_THROUGH: 'w',
    SHOOT: 'a',

    # Acciones en el Juego (Defensa)
    CHANGE_PLAYER: 'q',
    CALL_SECOND_DEFENDER: 'a', # Misma tecla que disparo

    # Acciones de Menú
    PAUSE_MENU: 'b',
    CONFIRM: 'enter',
    BACK: 'esc',
}

GAMEPAD_MAPPING = {
    # Movimiento y Navegación (D-Pad para menús, Stick para juego)
    'MOVE_UP': 'dpad_up',
    'MOVE_DOWN': 'dpad_down',
    'MOVE_LEFT': 'dpad_left',
    'MOVE_RIGHT': 'dpad_right',
    # NOTA: El movimiento del jugador con el stick izquierdo es analógico y se gestionará de forma diferente.

    # Acciones en el Juego (Ataque)
    SPRINT: 'right_trigger',       # RT
    PASS_SHORT: 'button_south',    # A (Xbox)
    PASS_HIGH: 'button_west',      # X (Xbox)
    PASS_THROUGH: 'button_north',  # Y (Xbox)
    SHOOT: 'button_east',          # B (Xbox)

    # Acciones en el Juego (Defensa)
    CHANGE_PLAYER: 'left_bumper',        # LB
    CALL_SECOND_DEFENDER: 'right_bumper',# RB

    # Acciones de Menú
    PAUSE_MENU: 'start_button',
    CONFIRM: 'button_south',       # A (Xbox)
    BACK: 'button_east',           # B (Xbox)
}

# Por defecto, el programa usará el mapeo de teclado.
# Esta variable ya no es necesaria, ya que la GUI gestiona el esquema activo.
# ACTIVE_CONTROL_SCHEME = KEYBOARD_MAPPING