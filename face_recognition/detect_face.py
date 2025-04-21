# face_recognition/detect_face.py

import cv2

# Cargar el modelo Haar Cascade para detección de rostros
face_cascade = cv2.CascadeClassifier(f"{cv2.data.haarcascades}haarcascade_frontalface_default.xml")

def detect_faces(frame):
    """
    Detecta rostros en un frame utilizando OpenCV Haar Cascades.

    :param frame: Imagen o frame en formato BGR (por ejemplo, desde cv2.VideoCapture)
    :return: Lista de rectángulos (x, y, w, h) que representan las caras detectadas.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
