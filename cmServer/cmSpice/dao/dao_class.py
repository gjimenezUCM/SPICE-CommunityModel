import pandas as pd


class DAO():
    """
    Superclass for all dao's
    """
    def __init__(self, route):
        self.data = ""
        self.route = route
        self.extractData()
        
        print("self.route: " + str(self.route))


    def extractData(self):
        """
        Class for data extraction from csv, json, api,...
        Read and assign or updates self.data value 
        """
        pass

    def getData(self):
        return self.data

    def getPandasDataframe(self):
        print("data: ")
        print(self.data)
        print("\n\n")
        return pd.read_json(self.data)
    

    