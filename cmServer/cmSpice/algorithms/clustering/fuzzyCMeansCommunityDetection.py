from fcmeans import FCM

class FuzzyCMeansCommunityDetection:

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
        metric :
            distanceMatrix
        n_clusters : int, optional
            The number of clusters to form as well as the number
        max_iter : int, optional
            Maximum number of iterations of the fuzzy C-means
        m : float, optional
            Degree of fuzziness
        error : float, optional
            Relative tolerance with regards to Frobenius norm of

        Returns
        -------
        list
            List with the clusters each element belongs to (e.g., list[0] === cluster the element 0 belongs to.) 
        """
        

        """
        FCM
        Attributes:
        ----------
        n_clusters (int) (5): The number of clusters to form as well as the number
            of centroids to generate by the fuzzy C-means.
        max_iter (int) (150): Maximum number of iterations of the fuzzy C-means
            algorithm for a single run.
        m (float) (2.0): Degree of fuzziness: $m \in (1, \infty)$.
        error (float) (1e-5): Relative tolerance with regards to Frobenius norm of
            the difference
            in the cluster centers of two consecutive iterations to declare
            convergence.
        random_state (Optional[int]) (None): Determines random number generation for
            centroid initialization.
            Use an int to make the randomness deterministic.
        trained (bool) (Field(False, const=True)): Variable to store whether or not the model has been
            trained.
        distance (euclidean): "euclidean", "cosine", "minkowski"
        """
        fcm = FCM(n_clusters=n_clusters, max_iter=150, m=2.0, error=1e-5)
        fcm.fit(distanceMatrix)
        clusters = fcm.predict(distanceMatrix)


        # fix values
        clusters = [len(clusters) if item == -1 else item for item in clusters]
        # Rename the clusters ids to avoid missing intermediate values
        uniqueLabels = set(clusters)      
        uniqueLabels = sorted(uniqueLabels)
        clusters = [uniqueLabels.index(label) for label in clusters]

        print("clusters:", clusters)
        return clusters
