"""
=============================================================
Example 2: Community detection using basic similarity measure
=============================================================

This example shows how to implement community detection based
on the similarity between a property of users. In addition, 
this example shows how to apply a basic similarity measure
to detect communities. Basic similarity metrics are detailed
in class SimilarityCommunityDetection.

This code detects up to 5 communities based on the emotions that
users felt watching artworks (information saved in users_emotions.json).

"""
import pandas as pd

from cmSpice.algorithms.clustering.similarityCommunityDetection import SimilarityCommunityDetection
from cmSpice.algorithms.similarity.emotionSimilarity import EmotionSimilarity

def main():

    # Paso 1: Cargamos los datos de las emociones
    #NOTE: Estos datos los obtenemos del User Model (en teoría)
    users_emotions_df = pd.read_json('../data/prado-dataset/users_emotions.json', orient='index')
    users_emotions_df.fillna(0.0, inplace=True)

    # Paso 2: Aplico el algortimo de detección de comunidades
    community_detection = SimilarityCommunityDetection(users_emotions_df)
    result = community_detection.calculate_communities(metric='euclidean', n_clusters=5)

    # Paso 3: Imprimo los resultados de la detección
    # NOTE: Esta información debemos almacenarla en el modelo de comunidades ??
    for user, community in result.items():
        print('User: {}, Community: {}'.format(user, community))


if __name__ == '__main__':
    main()