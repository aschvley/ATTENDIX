import cv2
from face_recognition.detect_face import detect_faces
from face_recognition.embedder import get_embedding

def main():
    print("🔵 Iniciando Attendix - Prueba de reconocimiento facial...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ No se pudo acceder a la cámara.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error al leer el frame de la cámara.")
            break

        # Detectar rostros en el frame
        faces = detect_faces(frame)

        for (x, y, w, h) in faces:
            # ✅ Recortamos el rostro del frame
            face_img = frame[y:y+h, x:x+w]

            # Redimensionamos a 160x160 para FaceNet
            face_img = cv2.resize(face_img, (160, 160))

            # Obtenemos el embedding
            embedding = get_embedding(face_img)

            print("🧠 Embedding generado (5 valores):", embedding[:5])

            # Dibujar el rectángulo sobre el rostro detectado
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Mostrar la imagen en tiempo real
        cv2.imshow("Attendix - Vista en tiempo real", frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("🟡 Saliendo...")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Attendix finalizado.")

if __name__ == "__main__":
    main()
