import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

import numpy as np
from config import RECOGNITION_THRESHOLD # si estás dentro de una carpeta como /database

def buscar_estudiante_por_embedding(embedding_actual):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre, embedding FROM estudiantes")
    estudiantes = cursor.fetchall()

    estudiante_encontrado = None
    distancia_minima = float('inf')

    for id_est, nombre, embedding_str in estudiantes:
        embedding_guardado = np.fromstring(embedding_str, sep=',')  # convertir string a vector
        distancia = np.linalg.norm(embedding_actual - embedding_guardado)

        if distancia < RECOGNITION_THRESHOLD and distancia < distancia_minima:
            distancia_minima = distancia
            estudiante_encontrado = {
                "id": id_est,
                "nombre": nombre,
                "distancia": distancia
            }

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
