# face_recognition/embedder.py
import cv2
import numpy as np
from face_recognition.embedder import get_embedding
from database.db import get_connection
import json

def generar_y_guardar_embeddings():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, nombre, cedula FROM estudiantes WHERE embedding = '[]' OR embedding IS NULL")
    estudiantes = cursor.fetchall()

    if not estudiantes:
        print("✅ Todos los estudiantes ya tienen embeddings.")
        return

    for estudiante in estudiantes:
        print(f"⚡ Generando embedding para {estudiante['nombre']} ({estudiante['cedula']})")
        
        # Cargar la imagen del estudiante (asegúrate de tener las imágenes guardadas)
        img_path = f"data/imagenes/{estudiante['cedula']}.jpg"
        img = cv2.imread(img_path)

        if img is None:
            print(f"❌ No se encontró la imagen para {estudiante['nombre']}.")
            continue

        rostro_embedding = get_embedding(img)

        if rostro_embedding is not None:
            embedding_json = json.dumps(rostro_embedding.tolist())  # Convertir a formato JSON
            cursor.execute("UPDATE estudiantes SET embedding = %s WHERE id = %s", (embedding_json, estudiante["id"]))
            conn.commit()
            print(f"✅ Embedding guardado para {estudiante['nombre']}.")
        else:
            print(f"⚠️ No se pudo generar embedding para {estudiante['nombre']}.")

    conn.close()
    print("🔹 Proceso completado.")

if __name__ == "__main__":
    generar_y_guardar_embeddings()
