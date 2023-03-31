# Authors: José Ángel Sánchez Martín
import networkx as nx
from itertools import product

class GraphCommunityDetection:

    def __init__(self, data):
        """Construct of SimilariyCommunityDetection objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of attributes names and
            values contain the attribute values for each element.
        """
        self.data = data
        
    def generateGraph(self, elements, distanceMatrix):
        """
        Generates the nx.graph encoding the data used to calculate communities
        
        Parameters
        ----------
        elements : np.array
            List of datapoints (self.data.index)
        distanceMatrix : np.ndarray
            Square matrix encoding the distance between datapoints
            
        Returns
        -------
        graph : nx.Graph
            Graph object where nodes are elements to search communities and
            edges are the relationships (distances) between nodes in graph.
            
        """
        # Step 3: Convert information in Graph object
        nodes = []
        edges = []
        print("len distance matrix")
        print(distanceMatrix)
        print(len(distanceMatrix))
        print(range(len(distanceMatrix)))
        
        pairs = product(range(len(distanceMatrix)),range(len(distanceMatrix)))
        print("graph generate graph")
        print(pairs)
        for p in pairs:
            print(p[0])
            print(p[1])
            from_id = elements[p[0]]
            to_id = elements[p[1]]
            print(from_id)
            print(to_id)
            print("\n")
            
            if not (from_id in nodes):
                nodes.append(from_id)
                
            if not (to_id in nodes):
                nodes.append(to_id)
            
            edges.append((from_id, to_id))
        
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        
        return G