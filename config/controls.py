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
    # Movimiento y Navegación (D-Pad para menús, Stick para juego)
    'MOVE_UP': 'dpad_up',
    'MOVE_DOWN': 'dpad_down',
    'MOVE_LEFT': 'dpad_left',
    'MOVE_RIGHT': 'dpad_right',
    # NOTA: El movimiento del jugador con el stick izquierdo es analógico y se gestionará de forma diferente.

    # Acciones en el Juego (Ataque)
    'SPRINT': 'right_trigger',       # RT
    'PASS_SHORT': 'button_south',    # A (Xbox)
    'PASS_HIGH': 'button_west',      # X (Xbox)
    'PASS_THROUGH': 'button_north',  # Y (Xbox)
    'SHOOT': 'button_east',          # B (Xbox)
    'TRICK': 'right_stick_press',    # Pulsar Stick Derecho (R3)
    'CLOSE_CONTROL': 'left_bumper',  # LB

    # Acciones en el Juego (Defensa)
    'CHANGE_PLAYER': 'left_bumper',        # LB
    'PRESSURE': 'button_south',            # A (Xbox)
    'SLIDE_TACKLE': 'button_west',         # X (Xbox)
    'CALL_SECOND_DEFENDER': 'right_bumper',# RB
    'GOALKEEPER_RUSH': 'button_north',     # Y (Xbox)

    # Acciones de Menú
    'PAUSE_MENU': 'start_button',
    'CONFIRM': 'button_south',       # A (Xbox)
    'BACK': 'button_east',           # B (Xbox)
    'CANCEL_ACTION': 'button_west',  # X (Xbox)
}

# Por defecto, el programa usará el mapeo de teclado.
ACTIVE_CONTROL_SCHEME = KEYBOARD_MAPPING