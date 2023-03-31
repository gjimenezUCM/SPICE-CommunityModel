import unittest
import json
from context import dao
import os, sys


from dao.dao_db_communities import DAO_db_community


class Test_community(unittest.TestCase):

    def setUp(self):
        self.dao = DAO_db_community()

    def tearDown(self):
        # self.dao.drop()
        self.dao.deleteCommunity("001")
        self.dao.deleteCommunity("002")
        self.dao.deleteCommunity("009")
        self.dao.deleteCommunity("123")

    def test_deleteCommunity(self):
        data = {"id": "001"}
        self.dao.insertCommunity(data)
        self.dao.deleteCommunity("001")
        response = self.dao.getCommunity("001")
        self.assertEqual(response, {})

    def test_add_and_getCommunity(self):
        data = {
            "id": "001",
            "explanation": "asdasdasda ggaf vasfopaor",
            "users": ["001", "002", "003"]
        }
        self.dao.insertCommunity(data)
        response = self.dao.getCommunity("001")
        self.assertEqual(response, data)
        self.dao.deleteCommunity("001")

    def test_add_and_getCommunities(self):
        data1 = {"id": "001"}
        data2 = {"id": "002"}
        self.dao.insertCommunity(data1)
        self.dao.insertCommunity(data2)
        response = self.dao.getCommunities()
        self.assertIn(data1, response)
        self.assertIn(data2, response)
        self.dao.deleteCommunity("001")
        self.dao.deleteCommunity("002")

    def test_replace(self):
        data = {"id": "001"}
        newCommunityValues = {"id": "009"}
        self.dao.insertCommunity(data)
        self.dao.replaceCommunity("001", newCommunityValues)
        response = self.dao.getCommunity("009")
        self.assertEqual(response.get("id"), "009")
        self.dao.deleteCommunity("009")

    def test_updates(self):
        data = {
            "id": "001",
            "explanation": "asdasdasda ggaf vasfopaor"
        }
        newCommunityExplanation = "Older than 70"
        self.dao.insertCommunity(data)
        self.dao.updateExplanation("001", "Older than 70")
        response = self.dao.getCommunity("001")
        self.assertEqual(response.get("explanation"), newCommunityExplanation)
        self.dao.deleteCommunity("001")

    def test_addUser(self):
        data = {
            "id": "123",
            "explanation": "asdasdasda ggaf vasfopaor",
            "users": ["001", "002", "003"]
        }
        newUser = "009"
        self.dao.insertCommunity(data)
        self.dao.addUserToCommunity("123", newUser)
        response = self.dao.getCommunityUsers("123")
        self.assertIn(newUser, response.get("users"))
        self.dao.deleteCommunity("123")

    def test_valueError(self):
        with self.assertRaises(ValueError):
            self.dao.getData()


if __name__ == '__main__':
    unittest.main()
