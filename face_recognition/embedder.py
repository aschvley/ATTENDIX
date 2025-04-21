# face_recognition/embedder.py

import cv2
import numpy as np
import json
from deepface import DeepFace
from database.db import get_connection

def get_embedding(image):
    """
    Genera el embedding de una imagen usando DeepFace con el modelo FaceNet512.
    
    :param image: Imagen en formato OpenCV (BGR).
    :return: Embedding como un vector numpy de 512 dimensiones o None si falla.
    """
    if image is None:
        return None

    try:
        # DeepFace acepta imágenes directamente como arrays
        embedding_info = DeepFace.represent(img_path=image, model_name="Facenet512", enforce_detection=False)
        embedding_vector = embedding_info[0]["embedding"]
        return np.array(embedding_vector)

    except Exception as e:
        print("❌ Error generando embedding:", e)
        return None


def generar_y_guardar_embeddings():
    """
    Busca los estudiantes sin embedding, genera el embedding usando DeepFace y lo guarda en la base de datos.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, nombre, cedula FROM estudiantes WHERE embedding = '[]' OR embedding IS NULL")
    estudiantes = cursor.fetchall()

    if not estudiantes:
        print("✅ Todos los estudiantes ya tienen embeddings.")
        return

    for estudiante in estudiantes:
        print(f"⚡ Generando embedding para {estudiante['nombre']} ({estudiante['cedula']})")

        img_path = f"data/imagenes/{estudiante['cedula']}.jpg"
        img = cv2.imread(img_path)

        if img is None:
            print(f"❌ No se encontró la imagen para {estudiante['nombre']}.")
            continue

        embedding = get_embedding(img)

        if embedding is not None:
            embedding_json = json.dumps(embedding.tolist())
            cursor.execute("UPDATE estudiantes SET embedding = %s WHERE id = %s", (embedding_json, estudiante["id"]))
            conn.commit()
            print(f"✅ Embedding guardado para {estudiante['nombre']}.")
        else:
            print(f"⚠️ No se pudo generar embedding para {estudiante['nombre']}.")

    conn.close()
    print("🔹 Proceso completado.")


if __name__ == "__main__":
    generar_y_guardar_embeddings()
