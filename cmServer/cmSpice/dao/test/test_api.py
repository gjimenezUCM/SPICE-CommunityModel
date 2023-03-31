import unittest
import json
from context import dao
import os, sys


from dao.dao_api import DAO_api
from dao.dao_linkedDataHub import DAO_linkedDataHub


class Test(unittest.TestCase):

    # __User DAO test__
    def test_api_updateUser(self):
        data_set = [{
            "id": "23",
            "userid": "23",
            "origin": "90e6d701748f08514b01",
            "source_id": "90e6d701748f08514b01",
            "source": "Content description",
            "pname": "DemographicGender",
            "pvalue": "F (for Female value)",
            "context": "application P:DemographicsPrep",
            "datapoints": 0
        }]

        _, response = DAO_api().updateUser(23, data_set)
        self.assertTrue(response.ok)

    def test_api_updateUser(self):
        _, response = DAO_api().userCommunities("44")
        self.assertTrue(response.ok)

    # __Community DAO test__
    def test_api_communityList(self):
        _, response = DAO_api().communityList()
        self.assertTrue(response.ok)

    def test_api_communityDescription(self):
        _, response = DAO_api().communityDescription("621e53cf0aa6aa7517c2afdd")
        self.assertTrue(response.ok)

    def test_api_communityUsers(self):
        _, response = DAO_api().communityUsers("621e53cf0aa6aa7517c2afdd")
        self.assertTrue(response.ok)

    def test_valueError(self):
        with self.assertRaises(ValueError):
            DAO_api().getData()

    # __LinkedDataHub__
    def test_linkedDataHub(self):
        dao = DAO_linkedDataHub("https://api2.mksmart.org/object/89b71c31-4bd3-44ad-9573-420e6320e945")
        _, response = dao.getData()
        self.assertTrue(response.ok)


if __name__ == '__main__':
    unittest.main()
