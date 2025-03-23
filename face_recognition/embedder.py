# face_recognition/embedder.py

import numpy as np
from keras_facenet import FaceNet

# Carga automática del modelo
embedder = FaceNet()

# Función que prepara la imagen de un rostro (ya recortado y alineado)
def get_embedding(face_img):
    # El embedder espera una lista de imágenes (aunque sea una sola)
    embeddings = embedder.embeddings([face_img])
    return embeddings[0]
