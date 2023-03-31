################################################################################
########################## Dominant Color Similarity ###########################
################################################################################
import numpy as np
import pandas as pd
import imageio as imio
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
import math
import os
import json

from cmSpice.core.similarity.utils import colorsys
from cmSpice.core.cache.files import getAbsDataFolderName
from cmSpice.core.similarity.artworks.similarity import Similarity

class DominantColorSimilarity(Similarity):
    """Class that calculates the dominant color similarity between two artworks.

    TODO: Añadir una referencia a la wiki donde se explique esta función de similitud?
    """

    def __init__(self, artworks_CSV=os.path.abspath(os.getcwd())+'/data/external/Prado_artworks_wikidata.csv'):
        """__init__ method to create an object to calculate the dominant color similarity.

        TODO: Es necesario cambiar el parámetro artwork_CSV. Deberiamos pasar un objeto DAO, no una ruta
        de fichero.

        Parameters
        ----------
        artworks_CSV : str, optional
            Path where is saved the artworks wikidata information used to obtain images of all artworks, 
            by default os.path.abspath(os.getcwd())+'/data/Prado_artworks_wikidata.csv'
        """
        super().__init__()
        self.__pics__ = pd.read_csv(artworks_CSV, index_col="wd:paintingID")
        self._loadCacheColorData()

    def _loadCacheColorData(self):
        # TODO: Revisar, esto debería estar conectado con el módulo de cache
        self._dominantColorDataCacheFilename = "artworkColors.json"

        with open(os.path.join(getAbsDataFolderName(self._dataFolderName),self._dominantColorDataCacheFilename)) as json_file:
            self._dominantColorByArtwork = json.load(json_file)

        for key, value in self._dominantColorByArtwork.items():
            frec = value['frequency']
            maxValue = 0
            maxIndex = -1
            for index, frecValue in frec.items():
                if frecValue>maxValue:
                    maxIndex = int(index)
                    maxValue = frecValue
            self._dominantColorByArtwork[key]['dominant_color'] = value['colors'][maxIndex]

    def _colorPercentage(self, pxLabels):
        n_pixels = len(pxLabels)
        counter = Counter(pxLabels)  # count how many pixels per cluster
        perc = {}

        # Crea el vector de % dividiendo el numero de pixels de un cluster con el total
        for i in counter:
            perc[i] = np.round(counter[i] / n_pixels, 2)
            
        perc = dict(sorted(perc.items()))
        return perc
    
    def _extractColors (self, url, nColors = 5, samplingRatio = 0.05):
        img = imio.imread(url)
        dim = img.shape
        img = img.reshape(-1, 3)
        
        nSamples = int(dim[0]*dim[1]*samplingRatio)

        # Hace Kmeans
        kmeans = KMeans(n_clusters=nColors)
        image_sample = shuffle(img, random_state=0)[:nSamples]
        clusters = kmeans.fit(image_sample)
        return clusters.cluster_centers_, clusters.labels_

    def _extractDominantColor(self, entity):     
        url = self.__pics__.loc[entity,'Image URL']
        colors, pxLabels = self._extractColors(url)
        perc = self._colorPercentage(pxLabels)
        max_color_key = max(perc, key=perc.get)
        max_color_rgb = colors[max_color_key]
        return colorsys.rgb_to_hsv(max_color_rgb[0], max_color_rgb[1], max_color_rgb[2])

    def _dominantColor(self, entity): 
        max_color_rgb = self._dominantColorByArtwork[entity]['dominant_color']
        return colorsys.rgb_to_hsv(max_color_rgb[0], max_color_rgb[1], max_color_rgb[2])

    def computeSimilarity(self, A, B):
        """Method to calculate the dominant color similarity between artwork A and artwork B.

        TODO: Ver si en esta función tenemos que pasar la métrica

        Parameters
        ----------
        A : str
            The first artwork to calculate the dominant color similarity.
        B : str
            The second artwork to calculate the dominant color similarity.

        Returns
        -------
        double
            Value of the dominant color similarity between artwork A and artwork B.
        """
        a = self._dominantColor(A)
        b = self._dominantColor(B)
        dh = min(abs(a[0]-b[0]), 360-abs(a[0]-b[0])) / 180.0
        ds = abs(a[1] - b[1])
        dv = abs(a[2] - b[2]) / 255.
        minS = min(a[1],b[1])
        #distance = math.sqrt(dh * dh + ds * ds + dv * dv) # Euclidean
        distance = math.sqrt(dv * dv + a[1]*a[1] + b[1]*b[1] - 2*a[1]*b[1]*dh) # Weighted euclidean
        #distance = math.sqrt(minS*minS*dh*dh + ds*ds + dv*dv) # Geodesic distance in HSV
        #distance = minS*dh + ds + dv # Weighted L1
        return 1. - distance
    
    def computeColor(self, entity):
        """Method to extract the dominant color of an artwork.

        TODO: Completar descripción
        Parameters
        ----------
        entity : int
            Identity of the artwork.

        Returns
        -------
        [type]
            [description]
        """
        url = self.__pics__.loc[entity,'Image URL']
        return self._extractColors(url)