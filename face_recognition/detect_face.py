# face_recognition/detect_face.py
import cv2

# Cargar el modelo de detección de rostros con f-string
face_cascade = cv2.CascadeClassifier(f"{cv2.data.haarcascades}haarcascade_frontalface_default.xml")

def detect_faces(frame):
    """Detecta rostros en un frame de video/imágen."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
