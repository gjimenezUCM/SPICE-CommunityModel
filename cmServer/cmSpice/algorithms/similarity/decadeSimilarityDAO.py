# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math

import re

from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO

class DecadeSimilarityDAO(SimilarityDAO):

    def __init__(self, dao, similarityFunction):
        """
        Similarity class for decades

        Parameters
        ----------
        dao : dao object class
            DAO which processes and provides the data required by the similarity measure.
        similarityFunction: json dict
            Encodes the similarity function parameters (column it is applied to, weight...)
        """
        super().__init__(dao, similarityFunction)

        # Change year column to legible format
        self.data[self.similarityColumn] = self.data[self.similarityColumn].apply(self.convertToYear)

        # Change NaN to decade 0
        self.data[self.similarityColumn].fillna(value=0, inplace = True)
        
        # Set max/min values for calculating distance between elements
        maxValue = self.data.loc[self.data[self.similarityColumn] != 0, self.similarityColumn].max()
        minValue = self.data.loc[self.data[self.similarityColumn] != 0, self.similarityColumn].min()

        # Set max/min decades
        self.maxDecade = self.convertYearToDecade(self.convertToYear(maxValue))
        self.minDecade = self.convertYearToDecade(self.convertToYear(minValue))

    def distanceItems(self, elemA, elemB):
        """
        Method to obtain the distance between two items

        Parameters
        ----------
        elemA : String
            First item
        elemB : String
            Second item

        Returns
        -------
        double
            Distance between the two elements.
        """
        if (elemA == 0 or elemB == 0):
            return 1.0
        else:
            yearA = self.convertToYear(elemA)
            yearB = self.convertToYear(elemB)

            decadeA = self.convertYearToDecade(yearA)
            decadeB = self.convertYearToDecade(yearB)

            normalizeDecadeA = (decadeA - self.minDecade) / (self.maxDecade - self.minDecade)
            normalizeDecadeB = (decadeB - self.minDecade) / (self.maxDecade - self.minDecade)

            return (abs(normalizeDecadeA - normalizeDecadeB))

    def convertToYear(self, date):
        date = str(date)
        # leave only words, years and ranges
        date = "".join(date.split(" /"))
        # 1. Find ranges
        ranges = re.findall("([12][0-9]{3})-([12][0-9]{3})", date)
        if ranges:
            numRanges = []
            for r in ranges:
                y1 = int(r[0])
                y2 = int(r[1])
                # Ranges are simplified to the middle value
                numRanges.append(int((y1+y2)/2))
            return int(sum(numRanges)/len(numRanges))
        else:
            # 2. If we find several years, we try to compute the middle value among them
            years = re.findall("([12][0-9]{3})", date)
            if years: 
                numYears = [int(y) for y in years]
                return int(sum(numYears)/len(numYears))
            else: 
                return None


    def convertYearToDecade(self,year):
        return int((year-1)/10) * 10

#-------------------------------------------------------------------------------------------------------------------------------
#   Dominant value (explanation) between 2 years
#-------------------------------------------------------------------------------------------------------------------------------
        
    def dominantValue(self, valueA, valueB):
        # Compute decadeA and decadeB associated to valueA, valueB (years)
        decadeA = str(self.convertYearToDecade(valueA))
        decadeB = str(self.convertYearToDecade(valueB))

        # Return both decades
        return [decadeA, decadeB]
    
    def dominantValueType(self):
        return "list"