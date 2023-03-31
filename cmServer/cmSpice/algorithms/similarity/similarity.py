# Authors: Guillermo Jimenez-Díaz
#          Jose Luis Jorro-Aragoneses
#          José Ángel Sánchez Martín

from itertools import product
import numpy as np

class Similarity:
    """Class to define the functions to be implemented to calculate
    the similarity between elements.
    """
    
    def __init__(self,data):
        """Construct of Similarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements
        
        """
        self.data = data

    def distance(self,elemA, elemB):
        """Method to obtain the distance between two element.

        Parameters
        ----------
        elemA : int
            Id of first element. This id should be in self.data.
        elemB : int
            Id of second element. This id should be in self.data.

        Returns
        -------
        double
            Distance between the two elements.
        """
        pass

    def similarity(self,elemA, elemB):
        """Method to obtain the similarity between two element.

        Parameters
        ----------
        elemA : int
            Id of first element. This id should be in self.data.
        elemB : int
            Id of second element. This id should be in self.data.

        Returns
        -------
        double
            Distance between the two elements.
        """
        #pass
        return 1 - self.distance(elemA,elemB)

    def matrix_distance(self):
        """Method to calculate the matrix of distance between all element included in data.

        Returns
        -------
        np.array
            Matrix that contains all similarity values.
        """
        users = self.data.index
        pairs = product(range(len(users)), repeat=2)

        matrix = np.zeros((len(users), len(users)))
        for p in pairs:
            dist = self.distance(users[p[0]], users[p[1]])
            matrix[p[0], p[1]] = dist

        # Reduce the matrix to 2 decimals
        matrix = np.round(matrix,2)
        
        self.distanceMatrix = matrix
        
        return matrix

    def matrix_similarity(self):
        """Method to calculate the matrix of similarity between all element included in data.

        Returns
        -------
        np.array
            Matrix that contains all similarity values.
        """
        users = self.data.index
        pairs = product(range(len(users)), repeat=2)

        matrix = np.zeros((len(users), len(users)))
        for p in pairs:
            dist = self.similarity(users[p[0]], users[p[1]])
            matrix[p[0], p[1]] = dist

        return matrix
    
    