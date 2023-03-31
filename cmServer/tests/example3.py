"""
============================================================
Example 3: Community detection using graphs based algorithms
============================================================

.

"""
import json
import networkx as nx

from cmSpice.algorithms.clustering.graphsCommunityDetection import GraphCommunityDetection


def main():

    # Step 1: Load emotion relations (two users felt same emotion in a same artwork)
    #NOTE: Estos datos los he preparado en un notebook. Hay que pensar como crear los grafos en el módulo
    f = open('../data/prado-dataset/emotions_graphs.json')
    emotion_relations = json.load(f)
    
    # Step 2: Select an emotion to search communities in the graph
    anger_relations = emotion_relations['anger']
    
    # Step 3: Convert information in Graph object
    nodes = []
    edges = []

    for row in anger_relations:
        from_id = row[0]
        to_id = row[1]
        extra = row[2]

        if not (from_id in nodes):
            nodes.append(from_id)

        if not (to_id in nodes):
            nodes.append(to_id)

        edges.append((from_id, to_id))

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Step 4: We apply community detection algorithmusing Markov clustering
    community_detection = GraphCommunityDetection(G)
    result = community_detection.calculate_communities(algorithm='Greedy') 

    # Step 5: Print communities detected by algorithm
    # NOTE: Esta información debemos almacenarla en el modelo de comunidades ??
    for user, community in result.items():
        print('User: {}, Community: {}'.format(user, community))

if __name__ == '__main__':
    main()