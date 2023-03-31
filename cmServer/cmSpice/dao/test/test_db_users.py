import unittest
import json
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from dao_db_users import DAO_db_users

from bson.json_util import dumps, loads


class Test_db_users(unittest.TestCase):

    def setUp(self):
        self.dao = DAO_db_users()


    def tearDown(self):
        # self.dao.drop()
        self.dao.deleteUser("001")
        self.dao.deleteUser("002")
        self.dao.deleteUser("003")


    """
    an'ade un usuario en la db, lo elimina y lo intenta leer
    """

    def test_deleteUser(self):
        user = {"userid": "001",
                "gender": "F"}
        self.dao.insertUser(user)
        self.dao.deleteUser("001")
        response = self.dao.getUser("001")
        self.assertEqual(response, {})

    def test_add_and_getUser(self):
        user = {
            "id": "xxx",
            "userid": "001",
            "origin": "aaa",
            "source_id": "bbb",
            "age": "22",
            "gender": "F",
            "hobby": "car"
        }
        self.dao.insertUser(user)
        response = self.dao.getUser("001")
        del response["id"]
        del user["id"]
        self.assertEqual(response, user)
        self.dao.deleteUser("001")

    def test_add_and_getUsers(self):
        user1 = {
            "id": "xxx",
            "userid": "001",
            "origin": "aaa",
            "source_id": "bbb",
            "age": "22",
            "gender": "F",
            "hobby": "bwm"
        }
        user2 = {
            "id": "xxx",
            "userid": "002",
            "origin": "aaa",
            "source_id": "bbb",
            "age": "18",
            "gender": "M",
            "hobby": "kia"
        }
        self.dao.insertUser(user1)
        self.dao.insertUser(user2)
        response = self.dao.getUsers()
        # print(user1)
        del response[0]["id"]
        del response[1]["id"]
        del user1["id"]
        del user2["id"]
        self.assertIn(user1, response)
        self.assertIn(user2, response)
        self.dao.deleteUser("001")
        self.dao.deleteUser("002")

    def test_update(self):
        user = {
            "id": "xxx",
            "userid": "001",
            "origin": "aaa",
            "source_id": "bbb",
            "age": "22",
            "gender": "F",
            "hobby": "bwm"
        }
        userOtherValues = {
            "id": "xxx",
            "userid": "001",
            "origin": "aaa",
            "source_id": "bbb",
            "age": "19",
            "gender": "M",
            "religion": "AA"
        }
        correctResponse = {
            'userid': '001',
            'origin': 'aaa',
            'source_id': 'bbb',
            'hobby': 'bwm',
            'gender': 'M',
            'age': '19',
            'religion': 'AA'
        }
        self.dao.insertUser(user)
        self.dao.updateUser(userOtherValues)
        response = self.dao.getUser("001")
        del response["id"]
        self.assertEqual(response, correctResponse)
        # self.dao.deleteUser("001")

    def test_replace(self):
        user = {
            "id": "xxx",
            "userid": "001",
            "origin": "aaa",
            "source_id": "bbb",
            "age": "22",
            "gender": "F",
            "hobby": "bwm"
        }
        newUser = {
            "userid": "001",
            "origin": "aaa",
            "source_id": "bbb",
            "age": "19",
            "gender": "M",
            "religion": "AA"
        }
        self.dao.insertUser(user)
        self.dao.replaceUser(newUser)
        response = self.dao.getUser("001")
        del response["id"]
        self.assertEqual(response, newUser)
        # self.dao.deleteUser("001")

    def test_valueError(self):
        with self.assertRaises(ValueError):
            self.dao.getData()


if __name__ == '__main__':
    unittest.main()
