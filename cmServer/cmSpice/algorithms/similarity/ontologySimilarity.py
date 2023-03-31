# Authors: José Ángel Sánchez Martín
from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO

from owlready2 import *

class OntologySimilarity(SimilarityDAO):
    
    def __init__(self, dao, similarityFunction = {}):
        """Construct of TaxonomySimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of taxonomy member and
            values contain the number of times that a taxonomy member is in an element.
        """
        super().__init__(dao,similarityFunction)
        # load ontology
        #onto_path.append("ontologies")
        self.onto = get_ontology(os.path.join(os.path.dirname(__file__), 'ontologies/' + self.similarityColumn.lower() + '.owl'))      

        self.onto.load()


    def distanceItems(self, ontologyValueA, ontologyValueB):
        """
        Method to obtain the distance between two ages.

        Parameters
        ----------
        ontologyValueA : String
            First ontology id
        ontologyValueB : String
            Second ontology id

        Returns
        -------
        double
            Distance between the two elements.
        """
        if (self.validOntologyValue(ontologyValueA) and self.validOntologyValue(ontologyValueB)):
            # Get ancestors chosen values
            ancestorsA = self.onto[ontologyValueA.capitalize()].ancestors()
            ancestorsB = self.onto[ontologyValueB.capitalize()].ancestors()

            # Intersection ancestors (common ancestors)
            commonAncestors = ancestorsA.intersection(ancestorsB)
            lowestCommonAncestor, lowestCommonAncestorLayer = self.getOntologyLowestCommonAncestor(commonAncestors)

            # Get distance
            sim = lowestCommonAncestorLayer / max(self.elemLayer(ancestorsA), self.elemLayer(ancestorsB))
            distance = 1 - sim
        else:
            distance = 1.0

        return distance

    def distanceValues(self, valueA, valueB):
        """Method to obtain the distance between two taxonomy members.

        Parameters
        ----------
        valueA : list
            List of materials ontology ids
        valueB : object
            List of materials ontology ids

        Returns
        -------
        double
            Distance between the two ontology lists.
        """
        try:

            # Some artworks have more than one material (separated by ,)
            ontologyValueListA, ontologyValueListB = self.getOntologyValueList(valueA, valueB)
            distance = self.distanceBetweenLists(ontologyValueListA, ontologyValueListB)
            return distance

        # One of the elements is not in the taxonomy
        except Exception as e:
            print("exception ontologyDistance")
            print(e)

            print("ontologyDistance")
            print(valueA)
            print(valueB)
            print("\n")

            print("ontologyDistance List")
            print(ontologyValueListA)
            print(ontologyValueListB)
            print("\n")

            print("distance1: " + str(distance))
            print("\n")


            return 1.0

    def distanceListElements(self, elementA, elementB):
        """
        Distance between two ontology values.
        Specialization of the inherited function for calculating distance between list members

        Parameters
        ----------
        elementA : Ontology class id
            String
        
        elementB : Ontology class id
            String

        Returns
        -------
        double
            Distance between the 2 ontology class labels
        """
        return self.getDistanceBetweenItems(elementA, elementB)

#-------------------------------------------------------------------------------------------------------------------------------
#   Auxiliar functions
#-------------------------------------------------------------------------------------------------------------------------------

    def validOntologyValue(self, value):
        value = value.capitalize()
        ontoValue = self.onto[value]
        return ontoValue is not None

    def getOntologyValueList(self, ontologyValueListA, ontologyValueListB):
        """
        ontologyValueListA = valueA.split(', ')
        ontologyValueListB = valueB.split(', ')
        if ('none' in ontologyValueListA):
            ontologyValueListA.remove('none')
        if ('none' in ontologyValueListB):
            ontologyValueListB.remove('none')
        
        return ontologyValueListA, ontologyValueListB
        """

        # Remove labels that are not in the ontology
        ontologyValueListA = [value for value in ontologyValueListA if self.validOntologyValue(value)]
        ontologyValueListB = [value for value in ontologyValueListB if self.validOntologyValue(value)]

        return ontologyValueListA, ontologyValueListB

    def getOntologyLowestCommonAncestor(self, commonAncestors):
        """
        Returns the lowest common ancestor among a list of ancestors given by an ontology.

        Parameters
        ----------
        commonAncestors : list
            List of common ancestors

        Returns
        -------
        object
            Lowest common ancestor
        """
        lowestAncestor = None
        lowestAncestorLayer = -1
        for ancestor in commonAncestors:
            ancestor_ancestors = ancestor.ancestors()
            ancestorLayer = self.elemLayer(ancestor_ancestors)
            if (ancestorLayer > lowestAncestorLayer):
                lowestAncestorLayer = ancestorLayer
                lowestAncestor = ancestor
            
        return lowestAncestor, lowestAncestorLayer

    def elemLayer(self,ancestors):
        return len(ancestors)


#-------------------------------------------------------------------------------------------------------------------------------
#   To calculate dominant value between two values (in order to explain communities)
#-------------------------------------------------------------------------------------------------------------------------------
    
    def dominantValue(self, valueA, valueB):
        explainableValues = []
        
        """
        print("dominant value ontology similarity")
        print(self.artworkA)
        print("\n")
        print(self.artworkB)
        print("\n")
        """

        try:
            ontologyValueListA, ontologyValueListB = self.getOntologyValueList(valueA, valueB)

            explainableValues.append(self.extractDominantValue(ontologyValueListA, ontologyValueListB, self.artworkA, self.artworkB))
            explainableValues.append(self.extractDominantValue(ontologyValueListB, ontologyValueListA, self.artworkB, self.artworkA))

        except Exception as e:
            print("exception")
            print(e)
            """
            print("ontology A: " + str(valueA))
            print("ontology B: " + str(ontologyValueB))
            """
            print("checking test")
            print("\n")

            raise Exception(e)
            
            """
            #print("longestPrefixElemB: " + str(longestPrefixElemB))
            #print("commonParent: " + str(commonParent))
            #print("maxLayer: " + str(maxLayer))
            """

        if (len(ontologyValueListA) > 0 and len(ontologyValueListB) > 0):
            pass
            #print("explanainable values")
            #print("valueA: " + str(ontologyValueListA))
            #print("valueB: " + str(ontologyValueListB))
            #print("\n")
            #print(explainableValues)
            #print("\n")    
        
        return explainableValues

    def extractDominantValue(self, ontologyValueListA, ontologyValueListB, artworkA, artworkB):
        explainableValues = []

        for ontologyValueA in ontologyValueListA:
            # Get most similar ontologyValueB in ontologyValueListB
            #ontologyValueB = self.mostSimilarOntologyValue(ontologyValueA, ontologyValueListB)
            ontologyValueB = self.mostSimilarListElement(ontologyValueA, ontologyValueListB)
            if (self.validOntologyValue(ontologyValueA) and self.validOntologyValue(ontologyValueB)):
                # Get ancestors chosen values
                ancestorsA = self.onto[ontologyValueA.capitalize()].ancestors()
                ancestorsB = self.onto[ontologyValueB.capitalize()].ancestors()

                # Intersection ancestors (common ancestors)
                commonAncestors = ancestorsA.intersection(ancestorsB)
                lowestCommonAncestor, lowestCommonAncestorLayer = self.getOntologyLowestCommonAncestor(commonAncestors)
                
                layerA = self.elemLayer(ancestorsA)
                layerB = self.elemLayer(ancestorsB)
                maxLayer = max(layerA, layerB)
                if (abs(lowestCommonAncestorLayer - maxLayer) <= 1 and lowestCommonAncestorLayer > 0):
                    # Explanation requires string (not Thing.class)
                    commonParent = lowestCommonAncestor.name.lower()
                    if (commonParent == "material"):
                        print("common parent root")
                        print("ontologyValueA: " + str(ontologyValueA))
                        print("ontologyValueB: " + str(ontologyValueB))
                        print("layerA: " + str(layerA))
                        print("maxLayer: " + str(maxLayer))
                        print("lowestCommonAncestorLayer: " + str(lowestCommonAncestorLayer))
                        print("abs: " + str(abs(lowestCommonAncestorLayer - maxLayer)))
                        print("ancestorsA: " + str(ancestorsA))
                        print("ancestorsB: " + str(ancestorsB))
                        print("\n")
                    commonParentDict = {}
                    commonParentDict[commonParent] = {}
                    # to_list is required when it is a dataframe
                    #commonParentDict[commonParent][ontologyValueA] = [ self.artworkA['id'].to_list()[0] ]
                    commonParentDict[commonParent][ontologyValueA] = [ artworkA['id'] ]

                    #commonParentDict[commonParent][ontologyValueA] = { "id": [self.artworkA['id'].to_list()[0]], "tittle": [self.artworkA['tittle'].to_list()[0]] }
                    if (ontologyValueB not in commonParentDict[commonParent]):
                        commonParentDict[commonParent][ontologyValueB] = []
                        #commonParentDict[commonParent][ontologyValueB] = {"id": [], "tittle": []}
                    
                    # to_list is required when it is a dataframe
                    #commonParentDict[commonParent][ontologyValueB].append( self.artworkB['id'].to_list()[0] )
                    commonParentDict[commonParent][ontologyValueB].append( artworkB['id'] )
                    
                    #commonParentDict[commonParent][ontologyValueB]['id'].append( self.artworkB['id'].to_list()[0] )
                    #commonParentDict[commonParent][ontologyValueB]['tittle'].append( self.artworkB['tittle'].to_list()[0] )

                    explainableValues.append(commonParentDict)

    
        return explainableValues
    
    
    
    
    