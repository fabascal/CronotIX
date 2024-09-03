import logging
import traceback
from functools import wraps
from flask import request, g
from datetime import datetime

# Configurar el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def log_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Obtener información del usuario si está autenticado
            user = getattr(g, 'user', None)
            user_info = f"User: {user.username if user else 'Anonymous'}"
            
            # Información de la solicitud
            logging.info(f"Función: {func.__name__} llamada por {user_info}")
            logging.info(f"Ruta: {request.path} | Método: {request.method}")

            # Llamar a la función original
            result = func(*args, **kwargs)

            # Loggear la salida si es necesario (puedes personalizar esto)
            logging.info(f"Función: {func.__name__} completada con éxito")

            return result

        except Exception as e:
            # Capturar el error y loggear la traza
            logging.error(f"Error en la función: {func.__name__}")
            logging.error(f"Error: {str(e)}")
            logging.error(f"Traza del error: {traceback.format_exc()}")

            # Propagar el error después de loggearlo
            raise e

    return wrapper
