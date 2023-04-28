import json
import pandas as pd
import re
from cmSpice.dao.dao_linkedDataHub import DAO_linkedDataHub
from cmSpice.dao.dao_api import DAO_api
import json

seedFilePath = 'seed.json'

# loader = ArtworkLoader(os.environ['TYPE'], True, "url", "uuid")
# outputData = loader.getArtworks()

class ArtworkLoader():

    def __init__(self, type=None, transform=False, url=None, uuid="xxx"):
        self.type = type
        self.transform = transform
        self.url = url
        self.uuid = uuid
        self.seedFile = None
        self.artworks = None
        self.seedFilePath = seedFilePath

        if self.type is None:
            raise Exception("type is not defined")

        # f = open(self.seedFilePath)
        # self.seedFile = json.load(f)
        daoApi = DAO_api()
        self.seedFile, _ = daoApi.getSeedFile()

        self.__readArtworks()
        if self.transform:
            self.__transform()

        if not self.__checkUsingSeedFile():
            # print("artworks validation with seed file failed")
            raise Exception("artworks validation with seed file failed")

    def __readArtworks(self):

        if self.url is None:
            f = open('localFile.json')
            self.artworks = json.load(f)
        else:
            dao = DAO_linkedDataHub(self.url, self.uuid)
            data, response = dao.getData()
            # print(response)

            # transform data from api format
            artworks = []
            for key in data[0].keys():
                if key.isnumeric():
                    artworks.append(data[0][key])

            self.artworks = artworks

    def __checkUsingSeedFile(self):
        for att in self.seedFile["artwork_attributes"]:
            for artwork in self.artworks:
                if att["on_attribute"]["att_name"] not in artwork:
                    print(att["on_attribute"]["att_name"])
                    return False
        return True

    def __transform(self):
        artifacts = pd.DataFrame(self.artworks)

        artifacts['Materials'] = artifacts.apply(lambda row: self.__transformMaterial(row), axis=1)

        if self.type == "GAM":
            artifacts['ApproxYear'] = artifacts['Year'].apply(self.__convertToYear)
            artifacts['ApproxYear'].fillna(value=0, inplace=True)
            artifacts['Decade'] = artifacts['ApproxYear'].apply(lambda v: int((v - 1) / 10) * 10)

        self.artworks = json.loads(artifacts.to_json(orient='records'))

        # rename keys
        dict = {
            "Author": "author",
            "Link": "image",
            "Title": "tittle",
            "Year": "year",
        }
        for row in self.artworks:
            for k, v in dict.items():
                if k in row.keys():
                    row[v] = row.pop(k)
                row["id"] = row["@id"]

    def __transformMaterial(self, row):
        """Returns a list of materials according to a dictionary for transformations
        It looks up the value of the 'Material_ and_echnique' columns and tries to transform it
        If no material is detected then it returns an empty list
        """
        if self.type == "GAM":
            materialTransformer = {
                "SU TELA": "canvas",
                "BRONZO": "bronze",
                "MARMO": "marble",
                "COMPENSATO": "plywood",
                "LEGNO": "wood",
                "TAVOLA": "wood",
                "CERAMICA": "ceramics",
                "CARTA": "paper",
                "CARTONE": "paper"
            }
            value = [] if "none" in row['Materials'] else row['Materials'].replace(" ", "").split(',')
            for key, val in materialTransformer.items():
                if key in row['Material_ and_echnique'].strip().upper():
                    value.append(val)
            return value
        elif self.type == "DMH":
            value = [] if "none" in row['Materials'] else row['Materials'].replace(" ", "").split(',')
            return value

    def __convertToYear(self, date):
        date = str(date)
        # leave only words, years and ranges
        date = "".join(date.split(" /"))
        # 1. Find ranges
        ranges = re.findall("([12][0-9]{3})-([12][0-9]{3})", date)
        if ranges:
            numRanges = []
            for r in ranges:
                y1 = int(r[0])
                y2 = int(r[1])
                # Ranges are simplified to the middle value
                numRanges.append(int((y1 + y2) / 2))
            return int(sum(numRanges) / len(numRanges))
        else:
            # 2. If we find several years, we try to compute the middle value among them
            years = re.findall("([12][0-9]{3})", date)
            if years:
                numYears = [int(y) for y in years]
                return int(sum(numYears) / len(numYears))
            else:
                return None

    def getArtworks(self):

        return self.artworks
