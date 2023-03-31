"""
==============================================================
Example 4: MNCN 2
==============================================================

"""
import pandas as pd

from cmSpice.algorithms.clustering.similarityCommunityDetection import SimilarityCommunityDetection
from cmSpice.algorithms.clustering.explainedCommunitiesDetection import ExplainedCommunitiesDetection

def transport_pollution_values(transport_polution):
    if transport_polution == 'High':
        return 2
    elif transport_polution == 'Medium':
        return 1
    elif transport_polution == 'Low':
        return 0
    
def transport_type_values(transport_type):
    if transport_type == 'Private':
        return 1
    else:
        return 0
    
def booleans_values(value):
    if value:
        return 1
    else:
        return 0

def main():

    # Load User profiles
    data_df = pd.read_csv('./data/MNCN/user_profiles_grouped.csv')

    data_df['Transport Pollution'] = data_df['Transport Pollution'].apply(transport_pollution_values)
    data_df['Transport Type'] = data_df['Transport Type'].apply(transport_type_values)
    data_df['Reduce Consumption'] = data_df['Reduce Consumption'].apply(booleans_values)
    data_df['Change Transport'] = data_df['Change Transport'].apply(booleans_values)
    data_df['Recycle'] = data_df['Recycle'].apply(booleans_values)

    attributes = {
        'Transport Pollution': ['Low (Walking, Bike)', 'Medium (Metro, Bus)', 'High (Car)'],
        'Transport Type': ['Public (Bus, Metro)', 'Private (Car, Bike, ...)'],
        'Reduce Consumption': ['No', 'Yes'],
        'Change Transport': ['No', 'Yes'],
        'Recycle': ['No', 'Yes']
    }

    # Select indexes from profiles
    indexes = ['Transport Pollution', 'Transport Type', 'Reduce Consumption', 'Change Transport', 'Recycle']

    # Filter indexes selected
    data = data_df[indexes]

    # Apply community detection algorithm
    community_detection = ExplainedCommunitiesDetection(data, SimilarityCommunityDetection, 'cosine')
    n_communities, users_communities = community_detection.search_all_communities(percentage=0.5)

    for c in range(n_communities):
        community_data = community_detection.get_community(c, percentage=0.5)
        print(community_data)


if __name__ == '__main__':
    main()