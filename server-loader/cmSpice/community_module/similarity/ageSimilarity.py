# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math

from cmSpice.community_module.similarity.similarityDAO import SimilarityDAO


HECHT_BELIEFS_E = ['Justify','Balanced','Oppose']


class AgeSimilarity(SimilarityDAO):

    def distanceValues(self, elemA, elemB):
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
    
        return (abs(elemA - elemB))

