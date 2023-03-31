# Authors: José Ángel Sánchez Martín

import networkx as nx

from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO
from cmSpice.algorithms.similarity.taxonomies.taxonomy import Taxonomy

class TaxonomySimilarityDAO(SimilarityDAO):
    
    def __init__(self, dao, similarityFunction = {}):
        """Construct of TaxonomySimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of taxonomy member and
            values contain the number of times that a taxonomy member is in an element.
        """
        super().__init__(dao,similarityFunction)
        self.taxonomy = Taxonomy(self.similarityColumn)
        
        #self.taxonomy = Taxonomy(self.data.columns.name)
        
    def getGraph():
        return self.taxonomy.getGraph()

    def elemLayer(self,elem):
        return self.taxonomy.getGraph().nodes[elem]['layer']
    
    def distanceItems(self,elemA,elemB):
        """Method to obtain the distance between two taxonomy members.

        Parameters
        ----------
        elemA : object
            Id of first element. This id should be in self.data.
        elemB : object
            Id of second element. This id should be in self.data.

        Returns
        -------
        double
            Similarity between the two taxonomy members.
        """
        try:
            commonAncestor = nx.lowest_common_ancestor(self.taxonomy.getGraph(),elemA,elemB)
            sim = self.elemLayer(commonAncestor) / max(self.elemLayer(elemA), self.elemLayer(elemB))
            return 1 - sim
        # One of the elements is not in the taxonomy
        except Exception as e:
            return 1

#-------------------------------------------------------------------------------------------------------------------------------
#   To calculate dominant value between two values (in order to explain communities)
#-------------------------------------------------------------------------------------------------------------------------------
    
    def dominantValue(self, valueA, valueB):
        try:
            commonAncestor = nx.lowest_common_ancestor(self.taxonomy.getGraph(), valueA, valueB)
            return [commonAncestor, commonAncestor]
        except Exception as e:
            return ['','']
    
    
    
    
    
    
    
    