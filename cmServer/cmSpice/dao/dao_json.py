import json

import os, sys
import pandas as pd


from cmSpice.dao.dao_class import DAO


class DAO_json(DAO):
    """
        DAO used to extract data from JSON files
    """

    def __init__(self, path):
        """
         :Parameters:
             path: path to file, Type: <class 'str'>
         """
        super().__init__(path)

    def extractData(self):
        with open(self.route, 'r', encoding='utf8') as f:
            self.data = json.load(f)


    def updateData(self, path):
        upd = None
        newList = []
        with open(path, 'r', encoding='utf8') as f:
            upd = json.load(f)
        for user in upd:
            user2 = self.__search(user["id"], self.data)[0]
            if user2 is not None:
                for key, value in user.items():
                    user2[key] = value
            else:
                newList.append(user)
        self.data = self.data + newList

    def __search(self, id, users):
        return [element for element in users if element['id'] == id]
    
    def getPandasDataframe(self):
        return pd.DataFrame(data = self.data)
