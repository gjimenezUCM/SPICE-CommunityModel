import json
import requests
from requests.auth import HTTPBasicAuth
import urllib.parse

from cmSpice.dao.dao_class import DAO

# To encode iconclassIDs with special characters (e.g., +)
#from urllib.parse import urlencode, quote_plus



class DAO_api_iconclass(DAO):
    """
    DAO used only for retrieving information from the iconclass API
    https://iconclass.org/docs#/default/json_list_json_get
    """
    def __init__(self, route=""):
        super().__init__(route)
        # self.route = route
        
    def responseProcessing(self, response):
        """Process response from API"""
        if response.status_code == 400:
            return
        self.data = response.json()
    
    
    # IDS that I couldn't find in the iconclass documentation.
    # 41C382(+53) banquet piece (+ round table) -> there is only up to (+9)
    
    def getIconclassText(self, iconclassID):
        """
        Method to obtain the text associated to an iconclassID

        Args:
            iconclassID: String

        Returns:
            iconclassText: String
        """
        #print("old ICONCLASSID: " + str(iconclassID))
        iconclassID = urllib.parse.quote(iconclassID.encode('utf8'))
        #print("new ICONCLASSID: " + str(iconclassID))
        
        
        urlRequest = "https://iconclass.org/json?notation={}".format(iconclassID)
        #print("urlRequest iconclass: " + str(urlRequest))
        response = requests.get(urlRequest)
        self.responseProcessing(response)
        #print("iconclass returned: " + str(self.data))
        
        result = self.data['result'][0]
        if (result is not None):
            iconclassText = result['txt']['en']
        else:
            iconclassText = 'Invalid Iconclass ID in the artworks database'
        
        
        #print("iconclassText: " + str(iconclassText))
        return iconclassText
        #return self.data, response
        
        