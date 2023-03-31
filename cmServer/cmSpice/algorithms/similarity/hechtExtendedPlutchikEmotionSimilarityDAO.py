
from cmSpice.algorithms.similarity.extendedPlutchikEmotionSimilarityDAO import ExtendedPlutchikEmotionSimilarityDAO

class HechtExtendedPlutchikEmotionSimilarityDAO(ExtendedPlutchikEmotionSimilarityDAO):


    def distanceValues(self, emotionsA, emotionsB):
        """
        Method to obtain the distance between two combination of emotions
        
        Compute distance between the first emotion in each list
        
        Parameters
        ----------
        emotionsA : String
            Emotions separated by ;
        emotionsB : String
            Emotions separated by ;

        Returns
        -------
        double
            Distance between the two combination of emotions.
        """
        if (isinstance(emotionsA, str) == False or isinstance(emotionsB, str) == False):
            return 1.0

        emotionA = emotionsA.split(";")[0].lower()
        emotionB = emotionsB.split(";")[0].lower()
        
        return self.getDistanceBetweenItems(emotionA,emotionB)

    def dominantInteractionAttribute(self, emotionsA, emotionsB):
        """
        Method to obtain the dominant value in each combination of emotions
        
        Parameters
        ----------
        emotionsDictA : dict
            Dict of Plutchik emotions (key: emotion; value: confidence level)
        emotionsDictB : dict
            Dict of Plutchik emotions (key: emotion; value: confidence level)

        Returns
        -------
        String
            Dominant emotion for A and B
        """
        emotionA = ""
        emotionB = ""

        if (isinstance(emotionsA, str) == True):
            emotionA = emotionsA.split(";")[0].lower()
        if (isinstance(emotionsB, str) == True):
            emotionB = emotionsB.split(";")[0].lower()   

        print("dominant interaction attribute")
        print(emotionsA)
        print(emotionA)
        print("\n")

        return [emotionA, emotionB]

    def dominantValue(self, emotionsA, emotionsB):  
        print("dominantValue")   
        return self.dominantInteractionAttribute(emotionsA, emotionsB) 