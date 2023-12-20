import numpy as np


def _prepare(vector1, vector2, norm=True):
    if isinstance(vector1, list):
        vector1 = np.array(vector1)
    if isinstance(vector2, list):
        vector2 = np.array(vector2)
    if norm:
        vector1 = normalize_vector(vector1)
        vector2 = normalize_vector(vector2)
    return vector1, vector2


def l2_distance(vector1, vector2, norm=True, use_sqrt=True):
    """
    Calculate the L2 distance between two vectors.
    Args:
        vector1 (list or numpy.ndarray):
            vector1
        vector2 (list or numpy.ndarray):
            vector2
        norm (bool):
            Whether to normalize the vectors before calculating the IP distance.
        use_sqrt (bool):
            Zilliz Cloud only calculates the value before applying the square root when Euclidean distance is chosen as the distance metric.
            If you want to get consistent results as zilliz cloud, set this value to False.

    Returns:
        l2_distance ('float'):
            The smaller it is, the more similar it is.
    """
    vector1, vector2 = _prepare(vector1, vector2, norm=norm)
    diff = vector1 - vector2
    if use_sqrt:
        l2_distance = np.sqrt(np.sum(diff ** 2))
    else:
        l2_distance = np.sum(diff ** 2)
    return l2_distance


def ip_distance(vector1, vector2, norm=True):
    """
    Calculate the IP distance between two vectors.
    Args:
        vector1 (list or numpy.ndarray):
            vector1
        vector2 (list or numpy.ndarray):
            vector2
        norm (bool):
            Whether to normalize the vectors before calculating the IP distance.

    Returns:
        ip_distance ('float'):
            [0, pi], The smaller it is, the more similar it is.
        cos_similarity ('float'):
            [-1, 1], The closer it is to 1, the more similar it is.
        inner_product ('float'):
            np.dot(vector1, vector2)
    """
    vector1, vector2 = _prepare(vector1, vector2, norm=norm)
    inner_product = np.dot(vector1, vector2)
    cos_similarity = inner_product / (calcu_norm(vector1) * calcu_norm(vector2))  # [-1, 1]
    ip_distance = np.arccos(cos_similarity)  # [0, pi]
    return ip_distance, cos_similarity, inner_product


def calcu_norm(vector):
    """
    l2 norm value of the vector.

    """
    vector = np.array(vector)
    norm = np.linalg.norm(vector)
    return norm


def normalize_vector(vector):
    """
    l2 normalize the vector.

    """
    norm = calcu_norm(vector)
    return vector / norm


if __name__ == '__main__':
    v1 = [2, 0]
    v2 = [-5, 0]
    print(ip_distance(v1, v2, norm=False))
