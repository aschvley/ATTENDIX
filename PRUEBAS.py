import cv2
import numpy as np
from keras_facenet import FaceNet
from sklearn.preprocessing import Normalizer

# Cargar el modelo FaceNet
model = FaceNet()

# Inicializar el clasificador de rostros de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Función para obtener los embeddings de la imagen facial
def get_embedding(face_pixels):
    # El modelo de FaceNet espera imágenes con un tamaño de 160x160 píxeles
    face_pixels = cv2.resize(face_pixels, (160, 160))
    face_pixels = np.expand_dims(face_pixels, axis=0)  # Añadir batch dimension
    face_pixels = face_pixels.astype('float32') / 255.0  # Normalización
    
    # Obtener los embeddings utilizando el modelo
    embedding = model.embeddings(face_pixels)
    return embedding

# Inicializar la cámara
cap = cv2.VideoCapture(1)

while True:
    # Capturar cada fotograma de la cámara
    ret, frame = cap.read()

    # Convertir la imagen a escala de grises para la detección de rostros
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectar rostros en la imagen
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Dibujar un rectángulo alrededor del rostro detectado
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Extraer la región del rostro
        face = frame[y:y+h, x:x+w]
        
        # Obtener el embedding para esta cara
        embedding = get_embedding(face)
        
        # Normalizar el embedding (si es necesario)
        normalizer = Normalizer(norm='l2')
        normalized_embedding = normalizer.transform(embedding)
        
        # Imprimir el embedding en la terminal
        print("Embedding del rostro:", normalized_embedding)

    # Mostrar el fotograma en una ventana
    cv2.imshow('Camera Feed', frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
