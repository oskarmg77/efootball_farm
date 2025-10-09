# config/controls.py

"""
Este archivo centraliza todos los mapeos de control para el juego.
Define las acciones abstractas y las asigna a teclas de teclado o botones de gamepad.
"""

# --- ACCIONES ABSTRACTAS DEL JUEGO ---
# Usamos nombres descriptivos para cada acción posible.

KEYBOARD_MAPPING = {
    # Movimiento y Navegación en Menús
    'MOVE_UP': 'up',
    'MOVE_DOWN': 'down',
    'MOVE_LEFT': 'left',
    'MOVE_RIGHT': 'right',

    # Acciones en el Juego (Ataque)
    'SPRINT': 'c',
    'PASS_SHORT': 'x',
    'PASS_HIGH': 'd',
    'PASS_THROUGH': 'w',
    'SHOOT': 'a',
    'TRICK': '3',
    'CLOSE_CONTROL': 'z',

    # Acciones en el Juego (Defensa)
    'CHANGE_PLAYER': 'q',
    'PRESSURE': 'x',          # Misma tecla que pase corto
    'SLIDE_TACKLE': 'd',      # Misma tecla que pase elevado
    'CALL_SECOND_DEFENDER': 'a', # Misma tecla que disparo
    'GOALKEEPER_RUSH': 'w',   # Misma tecla que pase en profundidad

    # Acciones de Menú
    'PAUSE_MENU': 'b',
    'CONFIRM': 'enter',
    'BACK': 'esc',
    'CANCEL_ACTION': 'd',
}

GAMEPAD_MAPPING = {
    # Movimiento y Navegación en Menús
    'MOVE_UP': 'dpad_up',
    'MOVE_DOWN': 'dpad_down',
    'MOVE_LEFT': 'dpad_left',
    'MOVE_RIGHT': 'dpad_right',

    # Acciones en el Juego (Ataque)
    'SPRINT': 'button_east',         # B
    'PASS_SHORT': 'button_south',    # A
    'PASS_HIGH': 'button_west',      # X
    'PASS_THROUGH': 'button_north',  # Y
    'SHOOT': 'button_east',          # B (Típicamente es X o B, lo mapeamos a B)
    'TRICK': 'right_stick_press',    # R3
    'CLOSE_CONTROL': 'right_trigger',# RT

    # Acciones de Menú
    'CONFIRM': 'button_south',       # A
    'BACK': 'button_east',           # B
}

# Por defecto, el programa usará el mapeo de teclado.
ACTIVE_CONTROL_SCHEME = KEYBOARD_MAPPING