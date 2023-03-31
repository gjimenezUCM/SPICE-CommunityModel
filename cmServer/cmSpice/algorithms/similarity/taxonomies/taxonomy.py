# Authors: José Ángel Sánchez Martín

import networkx as nx
import os

class Taxonomy:
    """Class to load the Taxonomy Graph Data
    """
    def __init__(self,taxonomyId):
        """Construct of Similarity objects.

        Parameters
        ----------
        taxonomyId : taxonomy identifier (e.g. country)
        """
        
        """
        print("\ntaxonomy")
        print(str(type(taxonomyId)))
        print(str(taxonomyId))
        """
        
        self.graph = nx.read_gml(os.path.join(os.path.dirname(__file__), 'taxonomyGraphs/' + taxonomyId.lower() + '.gml'))      
    
    def getGraph(self):
        """Get graph

        Parameters
        ----------
        """
        return self.graph
       