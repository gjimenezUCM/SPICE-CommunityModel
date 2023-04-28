# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math

from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO

class CenturySimilarity(SimilarityDAO):

    def __init__(self, dao, similarityFunction):
        """
        Similarity class for Centurys

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

        # Change NaN to Century 0
        self.data[self.similarityColumn].fillna(value=0, inplace = True)
        
        # Set max/min values for calculating distance between elements
        maxValue = self.data.loc[self.data[self.similarityColumn] != 0, self.similarityColumn].max()
        minValue = self.data.loc[self.data[self.similarityColumn] != 0, self.similarityColumn].min()

        # Set max/min Centurys
        self.maxCentury = self.convertYearToCentury(self.convertToYear(maxValue))
        self.minCentury = self.convertYearToCentury(self.convertToYear(minValue))

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

            CenturyA = self.convertYearToCentury(yearA)
            CenturyB = self.convertYearToCentury(yearB)

            normalizeCenturyA = (CenturyA - self.minCentury) / (self.maxCentury - self.minCentury)
            normalizeCenturyB = (CenturyB - self.minCentury) / (self.maxCentury - self.minCentury)

            return (abs(normalizeCenturyA - normalizeCenturyB))

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


    def convertYearToCentury(self,year):
        return int((year-1)/100) * 100

#-------------------------------------------------------------------------------------------------------------------------------
#   Dominant value (explanation) between 2 years
#-------------------------------------------------------------------------------------------------------------------------------
        
    def dominantValue(self, valueA, valueB):
        # Compute CenturyA and CenturyB associated to valueA, valueB (years)
        CenturyA = str(self.convertYearToCentury(valueA))
        CenturyB = str(self.convertYearToCentury(valueB))

        # Return both Centurys
        return [CenturyA, CenturyB]
    
    def dominantValueType(self):
        return "list"

