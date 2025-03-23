import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt

from face_recognition.detect_face import detect_faces
from face_recognition.embedder import get_embedding

from database.db import buscar_estudiante_por_embedding, registrar_asistencia

class AttendixApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendix - Reconocimiento Facial")
        self.setGeometry(100, 100, 800, 600)

        # Widgets
        self.image_label = QLabel("📷 Cámara no iniciada", self)
        self.image_label.setStyleSheet("background-color: #000; color: white; font-size: 18px;")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("🔵 Estado: Esperando acción...", self)
        self.start_button = QPushButton("Iniciar Reconocimiento")
        self.stop_button = QPushButton("Detener")

        # Eventos
        self.start_button.clicked.connect(self.start_camera)
        self.stop_button.clicked.connect(self.stop_camera)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer para actualizar frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.cap = None

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
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

        # Detectar rostros
        faces = detect_faces(frame)
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (160, 160))
            embedding = get_embedding(face_img)
            print("🧠 Embedding generado:", embedding[:5])

            # Dibujar rectángulo en el frame
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Convertir a QImage
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap)

        
    def closeEvent(self, event):
        self.stop_camera()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendixApp()
    window.show()
    sys.exit(app.exec_())
