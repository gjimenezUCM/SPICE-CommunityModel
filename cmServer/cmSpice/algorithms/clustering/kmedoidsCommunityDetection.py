# Authors: José Ángel Sánchez Martín
from sklearn_extra.cluster import KMedoids

class KmedoidsCommunityDetection:

    def __init__(self, data):
        """Construct of SimilariyCommunityDetection objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of attributes names and
            values contain the attribute values for each element.
        """
        self.data = data

    def calculate_communities(self, distanceMatrix='euclidean', n_clusters=2):
        """Method to calculate the communities of elements from data.

        Parameters
        ----------
        distanceMatrix : np.ndarray
            Square matrix encoding the distance between datapoints
        n_clusters : int, optional
            Number of clusters (communities) to search, by default 2
            Must be 2 or more. If it is lower, the algorithm doesn't work.

        Returns
        -------
        dict
            Dictionary with all elements and its corresponding community.
        """
        n_clusters = max(2, n_clusters)
        kmedoids = KMedoids(metric='precomputed',method='pam', n_clusters=n_clusters, init='k-medoids++')
        kmedoids.fit(distanceMatrix)
        
        # Sometimes, kmedoids returns a bugged result with missing intermediate clustersç
        # Example (8 is left): 
        # [14 11  2  7  0  3 12 11  3  1  5 13  3  3  3  5  0  3 11 11  2  6  4  1
        # 12  7  9  3  3  9  4  0 10  0  6  0  7 12  6  6  0  4  3]
        # Rename the ones above to a lower id
        uniqueLabels = set(kmedoids.labels_)      
        uniqueLabels = sorted(uniqueLabels)
        kmedoids.labels_ = [uniqueLabels.index(label) for label in kmedoids.labels_]
        

        return kmedoids.labels_