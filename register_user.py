import cv2
from face_recognition.detect_face import detect_faces
from face_recognition.embedder import get_embedding
from database.db import get_connection
import numpy as np

def registrar_estudiante(nombre, cedula, embedding):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = "INSERT INTO estudiantes (nombre, cedula, embedding) VALUES (%s, %s, %s)"
    embedding_str = str(embedding.tolist())  # Convertimos a string para TEXT
    cursor.execute(sql, (nombre, cedula, embedding_str))
    
    conn.commit()
    cursor.close()
    conn.close()

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara.")
        return

    print("🔵 Posiciona el rostro del estudiante frente a la cámara...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error al capturar la imagen.")
            break

        faces = detect_faces(frame)

        for (x, y, w, h) in faces:
            rostro = frame[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (160, 160))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow("Vista previa del rostro", frame)

            print("✅ Rostro detectado. Presiona 'c' para capturar y registrar.")
            key = cv2.waitKey(0)
            if key == ord("c"):
                embedding = get_embedding(rostro)

                nombre = input("👤 Ingresa el nombre completo del estudiante (MAYÚSCULAS): ").strip().upper()
                cedula = input("🆔 Ingresa la cédula (formato V-12345678): ").strip().upper()

                registrar_estudiante(nombre, cedula, embedding)
                print(f"✅ Estudiante {nombre} registrado con éxito.")
                break

        cv2.imshow("Cámara - Registrar estudiante", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()