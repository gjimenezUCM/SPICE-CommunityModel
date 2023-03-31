from sklearn.cluster import Birch
from sklearn.metrics import davies_bouldin_score

import numpy as np


class BirchCommunityDetection:

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

        print("calculating Birch algorithm")

        # # <hypertuning>

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

        # fixed_params = {}
        # param_grid = {
        #     "n_clusters": range(2, 12),
        #     "threshold": np.arange(0.01, 5, 0.1),
        #     "branching_factor": range(2, 11)
        # }

        # score = 9223372036854775807
        # bestParams = {}
        # betsLabels = 0
        # for params in make_generator(param_grid):
        #     params.update(fixed_params)
        #     # model = model( **params )
        #     model = Birch(**params)
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


        # davies_bouldin best score:  0.5567769283905423
        # with the next params:
        # {'branching_factor': 6, 'threshold': 1.11, 'n_clusters': 2}

        # # </hypertuning>

        model = Birch(threshold=1.11, branching_factor=6, n_clusters=n_clusters)
        model.fit(distanceMatrix)

        # db_index = davies_bouldin_score(distanceMatrix, model.labels_)
        # print("db_index:")
        # print(db_index)

        # Get clusters
        clusters = model.labels_
        print("number of clusters: ")
        print(clusters)
        
        return clusters
