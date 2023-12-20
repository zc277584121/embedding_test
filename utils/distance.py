import numpy as np


def l2_distance(vector1, vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)

    diff = vector1 - vector2

    l2_distance = np.sqrt(np.sum(diff ** 2))

    return l2_distance


def ip_distance(vector1, vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)

    dot_product = np.dot(vector1, vector2)

    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    ip_distance = np.arccos(dot_product / (norm1 * norm2))

    return ip_distance


def vector_norm(vector):
    vector = np.array(vector)

    norm = np.linalg.norm(vector)

    return norm
