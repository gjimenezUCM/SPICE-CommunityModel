import json
import requests
from requests.auth import HTTPBasicAuth

from cmSpice.dao.dao_class import DAO

class DAO_linkedDataHub(DAO):
    """
        DAO used to extract data from linked data hub
    """
    def __init__(self, route="https://api2.mksmart.org/object/89b71c31-4bd3-44ad-9573-420e6320e945", uuid="xxx"):
        self.uuid = uuid
        super().__init__(route)
        self.response = None

    def getData(self):
        return self.data, self.response

    def extractData(self):
        self.response = requests.get(self.route, auth=HTTPBasicAuth(self.uuid, self.uuid))
        if self.response.status_code == 200:
            self.data = self.response.json()
        else:
            self.data = ""
            raise Exception('LinkedDataHub response != "200"')

