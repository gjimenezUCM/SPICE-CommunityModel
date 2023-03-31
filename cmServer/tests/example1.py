"""
==============================================================
Example 1: Community detection using custom similarity measure
==============================================================

This example shows how to implement community detection based
on the similarity between a property of users. In addition, 
this example shows how to apply a custom similarity measure
to detect communities.

This code detects up to 5 communities based on the emotions that
users felt watching artworks (information saved in users_emotions.json).

"""
import pandas as pd

from context import cmSpice

def main():

    # Step 1: Load users emotions data
    #NOTE: Estos datos los obtenemos del User Model (en teoría)
    users_emotions_df = pd.read_json('../data/prado-dataset/users_emotions.json', orient='index')
    users_emotions_df.fillna(0.0, inplace=True)

    # Step 2: We apply community detection algorithm using a custom similarity measure (EmotionSimilarity)
    community_detection = cmSpice.algorithms.clustering.similarityCommunityDetection(users_emotions_df)
    result = community_detection.calculate_communities(metric=cmSpice.algorithms.similarity.emotionSimilarity, n_clusters=5)

    # Step 3: Print communities detected by algorithm
    # NOTE: Esta información debemos almacenarla en el modelo de comunidades ??
    for user, community in result.items():
        print('User: {}, Community: {}'.format(user, community))


if __name__ == '__main__':
    main()