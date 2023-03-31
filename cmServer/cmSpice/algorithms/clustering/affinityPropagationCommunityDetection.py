from sklearn.cluster import AffinityPropagation
from sklearn.metrics import davies_bouldin_score
import numpy as np

class AffinityPropagationCommunityDetection:

    def __init__(self, data):
        """Construct of opticsCommunityDetection. 

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of attributes names and
            values contain the attribute values for each element.
        """
        self.data = data

    def calculate_communities(self, distanceMatrix, n_clusters=2):
        """
        Method to calculate the communities of elements from data.

        Parameters
        ----------
        metric : str or Class, optional
            Metric used to calculate the distance between elements, by default 'euclidean'. It is
            possible to use a class with the same properties of Similarity.
        n_clusters : int, optional
            Number of clusters (communities) to search, by default 2

        Returns
        -------
        list
            List with the clusters each element belongs to (e.g., list[0] === cluster the element 0 belongs to.) 
        """

        clusters = []
        print("calculating optics algorithm")

        # <hypertuning>

        # def make_generator(parameters):
        #     # https://stackoverflow.com/a/55151423
        #     if not parameters:
        #         yield dict()
        #     else:
        #         key_to_iterate = list(parameters.keys())[0]
        #         next_round_parameters = {p: parameters[p]
        #                                  for p in parameters if p != key_to_iterate}
        #         for val in parameters[key_to_iterate]:
        #             for pars in make_generator(next_round_parameters):
        #                 temp_res = pars
        #                 temp_res[key_to_iterate] = val
        #                 yield temp_res

        # fixed_params = {"max_iter": 200}
        # param_grid = {
        #     "damping":  np.arange(0.5, 1.0, 0.01),
        #     "affinity": ["euclidean", "precomputed"],
        #     "convergence_iter": range(1, 20)
        # }

        # score = 9223372036854775807
        # bestParams = {}
        # betsLabels = 0
        # for params in make_generator(param_grid):
        #     params.update(fixed_params)
        #     # model = model( **params )
        #     model = AffinityPropagation(**params)
        #     model.fit(distanceMatrix)
        #     labels = model.labels_
        #     if len(set(labels)) < 2:
        #         continue  # si hay solo 1 cluster salta excepcion en davies_bouldin_score
        #     nScore = davies_bouldin_score(distanceMatrix, labels)
        #     print(params)
        #     print(nScore)
        #     print(labels)
        #     if nScore < score:
        #         score = nScore
        #         bestParams = params
        #         betsLabels = labels
        # print("davies_bouldin best score: ", score)
        # print("with the next params:")
        # print(bestParams)
        # print("labels:")
        # print(betsLabels)

        # davies_bouldin best score:  1.2061450970992438
        # with the next params:
        # {'convergence_iter': 7, 'affinity': 'euclidean', 'damping': 0.5, 'max_iter': 200}

        # </hypertuning>


        # run AffinityPropagation
        # model = AffinityPropagation(convergence_iter= 7, affinity="euclidean", damping= 0.5)

        clusters = []
        parameter = 0.5
        bestResult = 999
        best = [-1]
        while len(set(clusters)) != n_clusters and parameter < 1:
            # run dbscan
            model = AffinityPropagation(max_iter=500, damping=parameter, preference = -0.1)
            model.fit(distanceMatrix)

            # Get clusters
            clusters = model.labels_

            print("calculating AffinityPropagation algorithm")
            print("number of clusters: " + str(len(set(clusters))) + " expected:" + str(n_clusters))
            print("parameter: " + str(parameter))
            print("clusters:")
            print(clusters)
            print("\n")
            
            parameter += 0.01

            comp = abs(n_clusters-len(set(clusters)))
            if comp < bestResult:
                best = clusters
                bestResult = comp

            
        clusters = best
        print("best number of clusters: " + str(len(set(clusters))) + " expected:" + str(n_clusters))
        print(clusters)

        # db_index = davies_bouldin_score(distanceMatrix, clusters)
        # print("db_index:")
        # print(db_index)



        return clusters
