# Authors: José Ángel Sánchez Martín
from itertools import product
import numpy as np
import importlib
import json

from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO
from cmSpice.algorithms.similarity.complexSimilarityDAO import ComplexSimilarityDAO
from cmSpice.algorithms.similarity.interactionSimilarityDAO import InteractionSimilarityDAO

class CommunityModelSimilarity(SimilarityDAO):
    """
    Wrapper that calls the corresponding similarity class required by the Community Model
    """
    
    def __init__(self, dao, perspective):
        """Construct of Similarity objects.

        Parameters
        ----------
        dao : dao object class
            DAO which processes and provides the data required by the similarity measure.
        
        """
        super().__init__(dao)
        self.perspective = perspective

    def initializeComplexSimilarityMeasure(self):
        if ('Beliefs.beliefJ' in self.data.columns):
            # Remove artwork id similarity (from HECHT)
            similarityFunctions = [x for x in self.perspective['similarity_functions'] if x['sim_function']["on_attribute"]["att_name"] != "id" ]
            self.perspective['similarity_functions'] = similarityFunctions

            self.perspective['similarity_functions'].extend(self.perspective["interaction_similarity_functions"])
            self.perspective["interaction_similarity_functions"] = []

            similarityDict = self.perspective['similarity_functions']
            similarityMeasure = ComplexSimilarityDAO(
                self.dao, similarityDict)
        elif ('demographics.food' in self.data.columns):
            # Remove artwork id similarity (from HECHT)
            similarityFunctions = [x for x in self.perspective['similarity_functions'] if x['sim_function']["on_attribute"]["att_name"] != "id" ]
            self.perspective['similarity_functions'] = similarityFunctions
            self.perspective["interaction_similarity_functions"] = []
            
            if (len(self.perspective['similarity_functions']) <= 0):
                self.perspective['similarity_functions'] = [
                    {
                        "sim_function": {
                            "name": "DiscreteDistributionSimilarity",
                            "params": [],
                            "on_attribute": {
                                "att_name": "demographics.food",
                                "att_type": "String"
                            },
                            "dissimilar": False
                        }
                    }
                ]
            similarityDict = self.perspective['similarity_functions']
            similarityMeasure = ComplexSimilarityDAO(
                self.dao, similarityDict)
        else:
            similarityMeasure = InteractionSimilarityDAO(
                self.dao, self.perspective)

        return similarityMeasure, self.perspective
        
    