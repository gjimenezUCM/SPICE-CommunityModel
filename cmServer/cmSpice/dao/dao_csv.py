import csv, json

import os, sys
import pandas as pd

from cmSpice.dao.dao_class import DAO


class DAO_csv(DAO):
    """
    DAO for extracting data from csv files
    """
    def __init__(self, path):
        """
        :Parameters:
            path: path to file, Type: <class 'str'>
        """
        super().__init__(path)

    def extractData(self):
        pass
        """
        self.data = []
        with open(self.route, encoding="ISO-8859-1") as csvFile:
            reader = csv.reader(x.replace('\0', '') for x in csvFile)
            csvReader = csv.DictReader(reader)
            for rows in csvReader:
                self.data.append(rows)
        # self.data = json.dumps(self.data, sort_keys=True, indent=4)
        """
    
    def getPandasDataframe(self):
        self.data = pd.read_csv(self.route,delimiter=';')
        return self.data
        

        
        
        

