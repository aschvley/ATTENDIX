import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from face_recognition.embedder import get_embedding
from face_recognition.detect_face import detect_faces
from database.db import buscar_estudiante_por_embedding, registrar_asistencia
from deepface import DeepFace  # Para precargar modelo

# 🚀 Precargar el modelo solo una vez al inicio
model = DeepFace.build_model("Facenet")

class AttendixApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendix - Reconocimiento Facial")
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel("📷 Cámara no iniciada", self)
        self.image_label.setStyleSheet("background-color: #000; color: white; font-size: 18px;")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("🔵 Estado: Esperando acción...", self)
        self.start_button = QPushButton("Iniciar Reconocimiento")
        self.stop_button = QPushButton("Detener")

        self.start_button.clicked.connect(self.start_camera)
        self.stop_button.clicked.connect(self.stop_camera)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.cap = None
        self.frame_count = 0  # 🧠 Para escanear rostros cada N frames

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)  # 1 logitech, 0 laptop
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Menor resolución = mejor rendimiento
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        if not self.cap.isOpened():
            self.status_label.setText("❌ No se pudo acceder a la cámara.")
            return
        self.status_label.setText("🟢 Cámara iniciada. Escaneando rostros...")
        self.timer.start(30)

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.image_label.setText("📷 Cámara detenida.")
        self.status_label.setText("🟡 Esperando acción...")

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.status_label.setText("❌ Error al leer el frame.")
            return

        # 🔁 Solo procesamos cada 5 frames
        self.frame_count += 1
        if self.frame_count % 5 != 0:
            self._update_display(frame)
            return

        faces = detect_faces(frame)
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (160, 160))
            embedding = get_embedding(face_img, model=model)  # 
            Usar modelo precargado
            estudiante = buscar_estudiante_por_embedding(embedding)

            if estudiante:
                registrar_asistencia(estudiante["id"])
                self.status_label.setText(f"✅ {estudiante['nombre']} registrado.")
            else:
                self.status_label.setText("❌ Estudiante no reconocido.")

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        self._update_display(frame)

    def _update_display(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        qt_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()
