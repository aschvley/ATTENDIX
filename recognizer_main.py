import cv2
from face_recognition.detect_face import detect_faces
from face_recognition.embedder import get_embedding
from face_recognition.recognizer import recognize_face
from attendance.attendance import registrar_asistencia

def procesar_rostro(frame, ya_registrados):
    # sourcery skip: use-named-expression
    faces = detect_faces(frame)

    for (x, y, w, h) in faces:
        rostro = frame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (160, 160))

        embedding = get_embedding(rostro)
        estudiante = recognize_face(embedding)

        if estudiante:
            if estudiante['id'] not in ya_registrados:
                registrar_asistencia(estudiante['id'])
                ya_registrados.add(estudiante['id'])
                print(f"✅ Asistencia registrada: {estudiante['nombre']} ({estudiante['cedula']})")
            else:
                print(f"🔁 {estudiante['nombre']} ya fue registrado en esta sesión.")
            color = (0, 255, 0)
            label = estudiante['nombre']
        else:
            print("❌ Estudiante no reconocido.")
            color = (0, 0, 255)
            label = "Desconocido"

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

def iniciar_camara():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara.")
        return

    print("📷 Iniciando Attendix - Modo asistencia en vivo...")
    ya_registrados = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ No se pudo leer el frame de la cámara.")
            break

        procesar_rostro(frame, ya_registrados)
        cv2.imshow("Attendix - Reconocimiento Facial", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("🟡 Finalizando toma de asistencia.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Sesión terminada.")

def main():
    iniciar_camara()

if __name__ == "__main__":
    main()
