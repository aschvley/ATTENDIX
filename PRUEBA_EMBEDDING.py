import numpy as np

def cosine_similarity(emb1, emb2):
    return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

def euclidean_distance(emb1, emb2):
    return np.linalg.norm(np.array(emb1) - np.array(emb2))

def parse_embedding(embedding_str):
    """ Convierte una cadena sin comas en una lista de floats """
    return [float(x) for x in embedding_str.split()]

# 🔹 Definir los embeddings como strings sin comas
embedding_1_str = ""
embedding_2_str = ""

# 🔹 Convertir a listas de floats
embedding_1 = parse_embedding(embedding_1_str)
embedding_2 = parse_embedding(embedding_2_str)

# 🔹 Cálculo de similitud y distancia
cos_sim = cosine_similarity(embedding_1, embedding_2)
euc_dist = euclidean_distance(embedding_1, embedding_2)

# 🔹 Mostrar resultados
print(f"📊 Similitud del coseno: {cos_sim:.4f}")
print(f"📏 Distancia euclidiana: {euc_dist:.4f}")
