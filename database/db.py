import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import numpy as np
import json
from config import RECOGNITION_THRESHOLD

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def buscar_embedding_en_db(embedding_actual):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, nombre, embedding FROM estudiantes")
    estudiantes = cursor.fetchall()

    estudiante_encontrado = None
    distancia_minima = float('inf')

    print(f"➡️ Forma del embedding actual (al inicio de la búsqueda): {embedding_actual.shape}")

    for estudiante in estudiantes:
        embedding_json_str = estudiante.get('embedding')
        if embedding_json_str:
            try:
                embedding_guardado_lista = json.loads(embedding_json_str)
                embedding_guardado = np.array(embedding_guardado_lista)
                print(f"  - Forma del embedding guardado DESPUÉS de json.loads() y np.array(): {embedding_guardado.shape}")
                distancia = np.linalg.norm(embedding_actual - embedding_guardado)
                print(f"  - Distancia con {estudiante['nombre']}: {distancia}")  # <--- AÑADE ESTA LÍNEA

                if distancia < RECOGNITION_THRESHOLD and distancia < distancia_minima:
                    distancia_minima = distancia
                    estudiante_encontrado = {
                        "id": estudiante['id'],
                        "nombre": estudiante['nombre'],
                        "distancia": distancia
                    }
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Error al decodificar JSON del embedding: {e}")
        else:
            print("Se encontró un embedding vacío para este estudiante.")

    cursor.close()
    conn.close()
    return estudiante_encontrado

def registrar_asistencia(estudiante_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO asistencias (estudiante_id) VALUES (%s)", (estudiante_id,))
    conn.commit()
    cursor.close()
    conn.close()