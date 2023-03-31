import unittest
import json

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from dao_csv import DAO_csv
from dao_json import DAO_json
import pathlib


def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True


class Test_file(unittest.TestCase):

    def test_json(self):
        route = r"data/sesion_jueves_11.json"
        data = DAO_json(route).getData()
        self.assertTrue(validateJSON(json.dumps(data)))

    def test_json_update(self):
        file1, file2 = None, None
        path1 = r"data/test_add_value.json"
        path2 = r"data/test_update_value.json"
        dao = DAO_json(path1)
        dao.getData()
        dao.updateData(path2)
        dataUpdated = dao.getData()
        dataCheck = [{'id': '001',
                      'userid': '001',
                      'origin': '90e6d701748f08514b01',
                      'source_id': '90e6d701748f08514b01',
                      'pname': 'DemographicGender',
                      'pvalue': 'F (for Female value)',
                      'source': 'Content description',
                      'context': 'application P:DemographicsPrep',
                      'datapoints': 0},
                     {'id': '002',
                      'userid': '002',
                      'origin': '90e6d701748f08514b02',
                      'source_id': '90e6d701748f08514b02',
                      'pname': 'DemographicGender',
                      'pvalue': 'F (for Female value)',
                      'source': 'Content description',
                      'context': 'application P:DemographicsPrep',
                      'datapoints': 0},
                     {'id': '003',
                      'userid': '003',
                      'origin': '90e6d701748f08514b03',
                      'source_id': '90e6d701748f08514b03',
                      'pname': 'DemographicGender',
                      'pvalue': 'M (for Female value)'}
                     ]
        self.assertEqual(dataCheck, dataUpdated)

    def test_csv(self):
        route = r"data/semana_ciencia_2021.csv"
        print(pathlib.Path().resolve())
        data = DAO_csv(route).getData()
        self.assertTrue(validateJSON(json.dumps(data)))


if __name__ == '__main__':
    unittest.main()
