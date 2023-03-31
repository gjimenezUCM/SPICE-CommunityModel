import networkx as nx
from networkx.algorithms import community
import markov_clustering as mc


from cmSpice.algorithms.clustering.graphCommunityDetection import GraphCommunityDetection

class MarkovCommunityDetection(GraphCommunityDetection):

    def calculate_communities(self, distanceMatrix, n_clusters=2):
        """Method to calculate the communities of elements from data.

        Parameters
        ----------
        distanceMatrix : np.ndarray
            Square matrix encoding the distance between datapoints
        n_clusters : int, optional
            Number of clusters (communities) to search, by default 2

        Returns
        -------
        list
            List with the clusters each element belongs to (e.g., list[0] === cluster the element 0 belongs to.) 
        """
        self.graph = self.generateGraph(self.data.index,distanceMatrix)
        
        # Get adjacency matrix of graph
        adjMatrix = nx.to_numpy_matrix(self.graph)

        # prepare array for clusters
        size = max(len(distanceMatrix), len(distanceMatrix[0]))
        communities = [0] * size


        clusters = []
        parameter = 1
        bestResult = 999
        best = [-1]
        while len(set(clusters)) < n_clusters and parameter < 500:
            parameter += 0.1
            # print(adjMatrix)


            # run MCL with default parameters
            result = mc.run_mcl(adjMatrix, inflation=parameter)  
            # get clusters         
            clusters = mc.get_clusters(result)    
            # tranform format from 
            # [(1,3),(0),(2)] to [1,0,2,0]
            for i in range(len(clusters)):
                for j in clusters[i]:
                    communities[j] = i

            print("calculating markov algorithm")
            print("number of clusters: " + str(len(set(communities))) + " expected:" + str(n_clusters))
            print("parameter 'inflation': " + str(parameter))
            print("clusters:")
            print(communities)
            print("\n")

            comp = abs(n_clusters-len(set(clusters)))
            if comp < bestResult:
                best = communities
                bestResult = comp
            
        
        communities = best
        print("best number of clusters: " + str(len(set(communities))) + " expected:" + str(communities))
        print(communities)

        return communities
        
      