# face_recognition/recognizer.py

import numpy as np
import json
from database.db import get_connection
from config import RECOGNITION_THRESHOLD

def get_known_embeddings():
    """
    Obtiene todos los embeddings conocidos desde la base de datos.

    :return: Lista de diccionarios con id, nombre, cedula y embedding (como np.array)
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, cedula, embedding FROM estudiantes")

    conocidos = []
    for row in cursor.fetchall():
        try:
            emb_array = np.array(json.loads(row["embedding"]))  # Convertimos JSON a NumPy array
            conocidos.append({
                "id": row["id"],
                "nombre": row["nombre"],
                "cedula": row["cedula"],
                "embedding": emb_array
            })
        except Exception as e:
            print(f"❌ Error al convertir embedding del estudiante {row['nombre']}: {e}")

    conn.close()
    return conocidos


def recognize_face(embedding):
    """
    Compara el embedding actual con los embeddings conocidos.

    :param embedding: Embedding generado por DeepFace
    :return: Diccionario del estudiante reconocido o None si no hay coincidencia
    """
    estudiantes = get_known_embeddings()
    for estudiante in estudiantes:
        known_embedding = estudiante["embedding"]
        distancia = np.linalg.norm(embedding - known_embedding)
        if distancia < RECOGNITION_THRESHOLD:
            return estudiante
    return None
