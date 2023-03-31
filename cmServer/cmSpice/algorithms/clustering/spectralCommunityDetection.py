from sklearn.cluster import SpectralClustering
from sklearn.metrics import davies_bouldin_score
import numpy as np


class SpectralCommunityDetection:

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
        print("calculating SpectralClustering algorithm")

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

        # fixed_params = {"n_init": 1, "n_jobs": 24,  "n_neighbors": 10}
        # param_grid = {
        #     "n_clusters": range(2, 12), 
        #     "gamma":  np.arange(1, 10, 1),
        #     "affinity": ["nearest_neighbors", "rbf"],
        #     # "n_neighbors": range(5, 15),
        #     "degree": range(1, 5),
        #     "coef0": np.arange(1, 5, 1)
        # }

        # score = 9223372036854775807
        # bestParams = {}
        # betsLabels = 0
        # for params in make_generator(param_grid):
        #     params.update(fixed_params)
        #     # model = model( **params )
        #     model = SpectralClustering(**params)
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
        # {'coef0': 1, 'degree': 3, 'affinity': 'rbf', 'gamma': 8, 'n_clusters': 2, 'n_init': 1, 'n_jobs': 24, 'n_neighbors': 10}

        # # </hypertuning>

        model = SpectralClustering(n_clusters=n_clusters, n_init=20, coef0=1, degree=3, affinity="rbf", gamma=8)
        model.fit(distanceMatrix)

        # db_index = davies_bouldin_score(distanceMatrix, model.labels_)
        # print("db_index:")
        # print(db_index)

        # Get clusters
        clusters = model.labels_

        return clusters
