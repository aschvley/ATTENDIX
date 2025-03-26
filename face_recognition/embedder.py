# face_recognition/embedder.py

import cv2
import numpy as np
import json
from keras_facenet import FaceNet
from database.db import get_connection

# Inicializar el modelo FaceNet
embedder = FaceNet()

def get_embedding(image):
    """
    Genera el embedding de una imagen usando FaceNet.
    
    :param image: Imagen en formato OpenCV (BGR).
    :return: Embedding como un vector numpy de 512 dimensiones o None si falla.
    """
    if image is None:
        return None

    # Convertir BGR a RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Redimensionar la imagen a 160x160 (requerido por FaceNet)
    image = cv2.resize(image, (160, 160))

    # Normalizar los valores de píxeles a la escala esperada por FaceNet
    image = np.asarray(image, dtype=np.float32) / 255.0

    # Expandir la dimensión para que sea compatible con el modelo
    image = np.expand_dims(image, axis=0)

    # Obtener el embedding
    embedding = embedder.embeddings(image)

    return embedding[0]  # Devolver el primer (y único) embedding


def generar_y_guardar_embeddings():
    """
    Obtiene imágenes de estudiantes sin embedding, genera los embeddings y los guarda en la base de datos.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Seleccionar estudiantes sin embeddings registrados
    cursor.execute("SELECT id, nombre, cedula FROM estudiantes WHERE embedding = '[]' OR embedding IS NULL")
    estudiantes = cursor.fetchall()

    if not estudiantes:
        print("✅ Todos los estudiantes ya tienen embeddings.")
        return

    for estudiante in estudiantes:
        print(f"⚡ Generando embedding para {estudiante['nombre']} ({estudiante['cedula']})")
        
        # Cargar la imagen del estudiante
        img_path = f"data/imagenes/{estudiante['cedula']}.jpg"
        img = cv2.imread(img_path)

        if img is None:
            print(f"❌ No se encontró la imagen para {estudiante['nombre']}.")
            continue

        rostro_embedding = get_embedding(img)

        if rostro_embedding is not None:
            embedding_json = json.dumps(rostro_embedding.tolist())  # Convertir a JSON
            cursor.execute("UPDATE estudiantes SET embedding = %s WHERE id = %s", (embedding_json, estudiante["id"]))
            conn.commit()
            print(f"✅ Embedding guardado para {estudiante['nombre']}.")
        else:
            print(f"⚠️ No se pudo generar embedding para {estudiante['nombre']}.")

    conn.close()
    print("🔹 Proceso completado.")


if __name__ == "__main__":
    generar_y_guardar_embeddings()
