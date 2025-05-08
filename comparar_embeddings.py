import cv2
import numpy as np
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import json
from face_recognition.detect_face import detect_faces
from face_recognition.embedder import get_embedding

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def get_embedding_db(nombre_estudiante):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT embedding FROM estudiantes WHERE nombre = %s"
    cursor.execute(query, (nombre_estudiante,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    if resultado and resultado['embedding']:
        return np.array(json.loads(resultado['embedding']))
    else:
        return None

# --- Configura tu nombre tal como aparece en la base de datos ---
tu_nombre_en_db = "Camila Velázquez"  # Reemplaza con tu nombre exacto

# --- Inicializar la cámara ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

print("Presiona 's' para capturar un frame y comparar el embedding, o 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al leer el frame.")
        break

    cv2.imshow('Captura de Cámara (Presiona \'s\' para comparar)', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        faces = detect_faces(frame)
        if isinstance(faces, np.ndarray) and faces.ndim > 1 and faces.shape[1] == 4:
            # Si detect_faces devuelve un array de NumPy con las coordenadas
            x, y, w, h = faces[0]
            face_img = frame[y:y+h, x:x+w]
            face_img_resized = cv2.resize(face_img, (160, 160))
            embedding_actual = get_embedding(face_img_resized)

            embedding_db = get_embedding_db(tu_nombre_en_db)

            if embedding_db is not None:
                distancia = np.linalg.norm(embedding_actual - embedding_db)
                print(f"\nDistancia entre el embedding actual de la cámara y el de '{tu_nombre_en_db}' en la base de datos: {distancia}")
            else:
                print(f"Error: No se encontró el embedding para '{tu_nombre_en_db}' en la base de datos o está vacío.")
        elif isinstance(faces, list) and len(faces) > 0 and len(faces[0]) == 4:
            # Si detect_faces devuelve una lista de listas o tuplas con las coordenadas
            x, y, w, h = faces[0]
            face_img = frame[y:y+h, x:x+w]
            face_img_resized = cv2.resize(face_img, (160, 160))
            embedding_actual = get_embedding(face_img_resized)

            embedding_db = get_embedding_db(tu_nombre_en_db)

            if embedding_db is not None:
                distancia = np.linalg.norm(embedding_actual - embedding_db)
                print(f"\nDistancia entre el embedding actual de la cámara y el de '{tu_nombre_en_db}' en la base de datos: {distancia}")
            else:
                print(f"Error: No se encontró el embedding para '{tu_nombre_en_db}' en la base de datos o está vacío.")
        else:
            print("No se detectó ningún rostro en el frame.")

cap.release()
cv2.destroyAllWindows()