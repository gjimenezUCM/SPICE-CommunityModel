"""
==============================================================
Example 4: MNCN 1
==============================================================

"""
import pandas as pd

from cmSpice.algorithms.clustering.similarityCommunityDetection import SimilarityCommunityDetection
from cmSpice.algorithms.clustering.explainedCommunitiesDetection import ExplainedCommunitiesDetection

def main():

    # Load User profiles
    data_df = pd.read_csv('./data/MNCN/user_profiles.csv')

    # Select indexes from profiles
    indexes = list(range(1,16))

    # Filter indexes selected
    data = data_df.iloc[:,indexes]

    # Apply community detection algorithm
    community_detection = ExplainedCommunitiesDetection(data, SimilarityCommunityDetection, 'cosine')
    n_communities, users_communities = community_detection.search_all_communities(answer_binary=True, percentage=1.0)

    for c in range(n_communities):
        community_data = community_detection.get_community(c, answer_binary=True)
        print(community_data)


if __name__ == '__main__':
    main()