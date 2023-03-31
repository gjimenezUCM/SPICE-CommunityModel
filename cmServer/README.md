
# SPICE Community Model

The Community Model supports the social cohesion across groups, by the understanding of their differences and recognizing what they have in common. The community model is responsible for storing information about explicit communities that users belong to. Additionally, it creates the implicit communities inferred from user interactions and it computes the metrics needed to define the similarity (and dissimilarity) among group of users. The Community Model will support the recommender system in the variety and serendipity to the recommendation results, that will not be oriented to the typically popular contents or based on providing similar contents to the users (the so called, filter bubble) but to the inter-group similarities and the intra-group differences. 
It is implemented using [Python](https://www.python.org).

## Quick start


## Developing

- `ApiServer`: Files managing the communication between the CM-API and the  itself.
- `algorithms`:
    - `clustering`: Clustering algorithms. To add a new one, implement a new class following the format "prefix" + "CommunityDetection" where "prefix" is the algorithm name that is used by the perspectives. `explainedCommunityDetection` is a special algorithm that generates explanations using any clustering algorithm.
    - `similarity`: Contains similarity measures and additional information for complex similarity measures (like taxonomies and tables). To add a new one, implement a new class inheriting from SimilarityDAO (in `similarityDAO.py`).
- `core`: Files managing the whole process of generating communities, from the input of the data to the generation of the data objects encoding the clustering results and its documentation in the database. They can be found inside /communityModel folder.
- `dao`: Includes the required classes to communicate with the database, with the Linked Data Hub, and to abstract the access to other file formats.

## License

The content of this repository is distributed under [Apache 2.0 License](LICENSE).