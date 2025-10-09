# agent/navigation.py

# Importamos el controlador de input y las acciones
from core.input_controller import execute_action
from config.controls import ACTION_DOWN, ACTION_ACCEPT


def select_second_option_on_menu():
    """
    Ejemplo de una función de navegación.
    Baja una vez y acepta.
    """
    print("Navegando al segundo elemento del menú.")

    # 2. Llama a execute_action con la acción abstracta
    execute_action(ACTION_DOWN)

    # Podrías añadir una pequeña pausa
    # time.sleep(0.5)

    execute_action(ACTION_ACCEPT)