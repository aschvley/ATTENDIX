# para obtener embeddings de las fotos!

from deepface import DeepFace
import numpy as np

def obtener_embedding_consola(ruta_imagen, model_name="ArcFace"):
    """
    Obtiene el embedding facial de una imagen y lo imprime en la consola
    como un string separado por comas.

    Args:
        ruta_imagen (str): Ruta de la imagen.
        model_name (str): Nombre del modelo de DeepFace a utilizar.
    """
    try:
        embedding_list = DeepFace.represent(img_path=ruta_imagen, model_name=model_name, enforce_detection=True)
        if embedding_list:
            embedding_array = embedding_list[0]['embedding']
            embedding_str = ",".join(map(str, embedding_array))
            print("Embedding facial:")
            print(embedding_str)
            print(f"\nLongitud del embedding: {len(embedding_array)}")
        else:
            print(f"No se detectaron rostros en la imagen: {ruta_imagen}")
    except Exception as e:
        print(f"Ocurrió un error al procesar la imagen {ruta_imagen}: {e}")

# Ejemplo de uso para una foto específica
ruta_de_la_foto = r"C:\Users\Camila\Desktop\database\foticos\5129641778947927974.jpg"  # ¡Reemplaza con la ruta de tu foto!

obtener_embedding_consola(ruta_de_la_foto)