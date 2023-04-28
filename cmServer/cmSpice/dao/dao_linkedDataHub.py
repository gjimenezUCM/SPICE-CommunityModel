import json
import requests
from requests.auth import HTTPBasicAuth

from cmSpice.dao.dao_class import DAO

class DAO_linkedDataHub(DAO):
    """
        DAO used to extract data from linked data hub
    """

    def __init__(self, route="xxx", uuid="xxx"):
        self.uuid = uuid
        super().__init__(route)
        # self.response = None
        if route == "xxx" or uuid == "xxx":
            raise Exception("Route or uuid is not defined")

    def getData(self):
        return self.data, self.response

    def extractData(self):
        self.response = requests.get(self.route, auth=HTTPBasicAuth(self.uuid, self.uuid))
        if self.response.status_code == 200:
            self.data = self.response.json()
        else:
            self.data = ""
            raise Exception('LinkedDataHub response != "200"')
