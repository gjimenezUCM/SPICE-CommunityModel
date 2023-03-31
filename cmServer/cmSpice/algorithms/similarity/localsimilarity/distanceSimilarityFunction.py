# Authors: Jose Luis Jorro-Aragoneses

from cmSpice.algorithms.similarity.similarity import Similarity

class DistanceSimilarity(Similarity):
    """Similarity function based on the distance between two numbers.
    For example, similarity based on the distance between two years.
    """

    def __init__(self):
        pass

    def distance(elemA, elemB):
        return super().distance(elemB)

    def similarity(elemA, elemB):
        return super().similarity(elemB)

    def matrix_similarity(self):
        pass

    def matrix_distance(self):
        pass    