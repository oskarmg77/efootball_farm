import google.generativeai as genai
import json
from PIL import Image

class GeminiVisionAnalyzer:
    """
    Analiza capturas de pantalla del juego eFootball utilizando la API de Gemini.
    """

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("La API Key de Gemini no ha sido configurada.")
        genai.configure(api_key=api_key)
        # Usamos el nuevo modelo, más rápido y económico
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        self.prompt = self._build_prompt()

    def _build_prompt(self) -> str:
        """
        Construye el prompt que se enviará a Gemini.
        Este prompt es clave para obtener una respuesta estructurada y precisa.
        """
        return """
        Analiza esta captura de pantalla del videojuego eFootball. Tu objetivo es actuar como un asistente de visión para un bot.
        Identifica el menú o pantalla actual y todas las opciones seleccionables.
        Proporciona tu respuesta exclusivamente en formato JSON.

        El JSON debe tener la siguiente estructura:
        {
          "current_screen": "nombre_de_la_pantalla",
          "selected_option": "texto_de_la_opcion_actualmente_seleccionada",
          "selectable_options": [
            {
              "option_name": "nombre_opcion_1",
              "coordinates": {"x": "centro_x", "y": "centro_y"}
            },
            {
              "option_name": "nombre_opcion_2",
              "coordinates": {"x": "centro_x", "y": "centro_y"}
            }
          ]
        }

        Ejemplos de 'current_screen': 'main_menu', 'game_plan', 'match_settings', 'in_match_pause_menu'.
        Si no puedes identificar la pantalla o no hay opciones, devuelve valores nulos o listas vacías.
        No incluyas explicaciones, solo el objeto JSON.
        """

    def analyze_image(self, image: Image.Image) -> dict | None:
        """
        Envía una imagen a la API de Gemini y parsea la respuesta JSON.

        Args:
            image (Image.Image): La imagen a analizar.

        Returns:
            dict | None: Un diccionario con la información parseada o None si falla.
        """
        try:
            response = self.model.generate_content([self.prompt, image])

            # Limpiar la respuesta para asegurar que solo contiene el JSON
            json_text = response.text.strip().replace("```json", "").replace("```", "")

            # Parsear la respuesta JSON
            parsed_data = json.loads(json_text)
            return parsed_data

        except json.JSONDecodeError as e:
            print(f"Error al decodificar la respuesta JSON de Gemini: {e}")
            print(f"Respuesta recibida: {response.text}")
            return None
        except Exception as e:
            print(f"Ocurrió un error al analizar la imagen con Gemini: {e}")
            return None