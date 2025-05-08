# para obtener embeddings de la camara!
import cv2
import numpy as np
from face_recognition.detect_face import detect_faces
from face_recognition.embedder import get_embedding
import json

# --- Inicializar la cámara ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

print("Presiona 's' para capturar un frame, detectar el rostro y mostrar su embedding en la terminal (formato para base de datos), o 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al leer el frame.")
        break

    cv2.imshow('Captura de Cámara (Presiona \'s\' para obtener embedding)', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        faces = detect_faces(frame)
        if isinstance(faces, np.ndarray):
            if faces.size > 0:
                # Asumiendo que detect_faces devuelve un array donde cada fila es un rostro [x, y, w, h]
                (x, y, w, h) = faces[0].astype(int)
                face_img = frame[y:y+h, x:x+w]
                face_img_resized = cv2.resize(face_img, (160, 160))
                embedding_actual = get_embedding(face_img_resized)

                print("\nEmbedding del rostro detectado: ", end="")
                print(json.dumps(embedding_actual.tolist(), separators=(',', ':')), end="")
                print() # Añade una nueva línea al final para la siguiente operación
            else:
                print("No se detectó ningún rostro en el frame.")
        elif isinstance(faces, list):
            if len(faces) > 0:
                # Asumiendo que detect_faces devuelve una lista de listas o tuplas [x, y, w, h]
                (x, y, w, h) = map(int, faces[0])
                face_img = frame[y:y+h, x:x+w]
                face_img_resized = cv2.resize(face_img, (160, 160))
                embedding_actual = get_embedding(face_img_resized)

                print("\nEmbedding del rostro detectado: ", end="")
                print(json.dumps(embedding_actual.tolist(), separators=(',', ':')), end="")
                print() # Añade una nueva línea al final para la siguiente operación
            else:
                print("No se detectó ningún rostro en el frame.")
        else:
            print("No se detectó ningún rostro en el frame.")

cap.release()
cv2.destroyAllWindows()