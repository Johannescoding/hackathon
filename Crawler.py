"""Data-Crawler for hackathon. Author: Tim"""

import json
import requests
from my_functools import download_wrapper

class Crawler:
    """Currently supported: kita, schulen, stadtteile"""

    
    def __init__(self):
        self.version = "beta"
        self.kita_link = "https://geoportal.stadt-koeln.de/arcgis/rest/services/Stadtplanthemen/MapServer/9/query?geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=&where=objectid%20is%20not%20null&time=&returnCountOnly=false&returnIdsOnly=false&returnGeometry=true&maxAllowableOffset=&outSR=4326&outFields=%2A&f=json"
        self.schulen_link = "https://geoportal.stadt-koeln.de/arcgis/rest/services/Stadtplanthemen/MapServer/6/query?text=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=&where=objectid%20is%20not%20null&time=&returnCountOnly=false&returnIdsOnly=false&returnGeometry=true&maxAllowableOffset=&outSR=4326&outFields=%2A&f=json"
        self.stadtteile_link = "https://geoportal.stadt-koeln.de/arcgis/rest/services/Stadtgliederung_15/MapServer/1/query?where=objectid%20is%20not%20null&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=%2A&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=4326&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson"
        self.stadtviertel_link = "https://geoportal.stadt-koeln.de/arcgis/rest/services/Stadtgliederung_15/MapServer/2/query?where=objectid%20is%20not%20null&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=%2A&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=4326&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson"
        self.adressen_link = "https://geoportal.stadt-koeln.de/arcgis/rest/services/Adresse_15/MapServer/0/query?where=objectid%20is%20not%20null&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=%2A&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=4326&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson"
        self.behindertenparkplatz_link = "https://geoportal.stadt-koeln.de/arcgis/rest/services/Stadtplanthemen/MapServer/0/query?text=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=&where=objectid%20is%20not%20null&time=&returnCountOnly=false&returnIdsOnly=false&returnGeometry=true&maxAllowableOffset=&outSR=4326&outFields=%2A&f=json"
        
        self.__beta_tester()


    @download_wrapper
    def get_behindertenparkplatz_dict(self):
        """"returns a dict. key: stadtteil, value: number of behindertanparkplätze"""
        
        stadtteile_dict = self._dict_helper(self.behindertenparkplatz_link, "behindertenparkplatz")             
        return stadtteile_dict
        

    @download_wrapper
    def get_schulen_dict(self):
        """returns a dict. key: stadtteil, value: number of schulen"""
        stadtteile_dict = self._dict_helper(self.schulen_link)             
        return stadtteile_dict

    
    @download_wrapper
    def get_kita_dict(self):
        """returns a dict. key: stadtteil, value: number of kitas"""

        stadtteile_dict = self._dict_helper(self.kita_link)             
        return stadtteile_dict


    @download_wrapper
    def get_stadtteile_list(self):
        """returns a list containing all stadtteile"""
    
        json_as_dict = self._json_to_python_object(self.stadtteile_link)

        # get feature list
        feature_list = json_as_dict["features"]

        stadtteile_list = list()
        # iterate over feature list and extract the name
        for feature in feature_list:
            stadtteile_list.append(feature["attributes"]["NAME"])
            
        return stadtteile_list

    @download_wrapper
    def get_strassen_list(self):
        """liste mit straßen. Ultra schlechter Datensatz!!!"""

        self.__warning_bad_data_quality()
        
        json_as_dict = self._json_to_python_object(self.stadtteile_link)

        # get feature list
        feature_list = json_as_dict["features"]

        stadtteile_list = list()
        # iterate over feature list and extract the name
        for feature in feature_list:
            stadtteile_list.append(feature["attributes"]["NAME"])
            
        return stadtteile_list


    @download_wrapper
    def get_straßen_stadtteil_dict(self):
        """returns a dict with streets as key and stadtteil as value"""

        self.__warning_bad_data_quality()
        
        json_as_dict = self._json_to_python_object(self.adressen_link)

        # get feature list
        feature_list = json_as_dict["features"]

        straßen_stadtteil_dict = dict()
        # iterate over feature list and extract the name
        for feature in feature_list:
            straßen_stadtteil_dict[feature["attributes"]["STRASSE"]] = feature["attributes"]["STADTTEIL"]
            
        return straßen_stadtteil_dict
       

    def _json_to_python_object(self, link):
        """retreives data from link and converts it to json"""

        # request data from website
        __response = requests.get(link)

        # extract content from response object. Is in bytes form containing json information
        __content = __response.content

        #convert from byte-json-object to python object
        __python_object_representing_json = json.loads(__content)
        
        return  __python_object_representing_json


    def _setup(self, json_dict):
        """
        Returns a tuple: (feature_list, stadtteile_dict)
        Takes the json_dict as argument and extracts the features(first tuple component)
        The second component is a dict with all stadtteile as keys initialized with 0
        """

        # list with features of json_dict
        feature_list = json_dict["features"]

        # create stadtteile_dict
        stadtteile_list = self.get_stadtteile_list()
        stadtteile_dict = { anzahl : 0 for anzahl in stadtteile_list } # creates a dict from list with dafaultvalue 0
        
        return (feature_list, stadtteile_dict)

    def _dict_helper(self, link, modus = "behindertenparkplatz"):
        """returns a dict. containing stadtteile and value"""
        
        # get json with meta and features
        mother_json = self._json_to_python_object(link)

        # extract the important information 
        feature_list, stadtteile_dict = self._setup(mother_json)
        
        for feature in feature_list:
            stadtteil = feature["attributes"]["STADTTEIL"]

            if modus == "behindertenparkplatz":
                amount = feature["attributes"]["ANZAHL"]
                try:
                    stadtteile_dict[stadtteil] += amount
                except KeyError:
                    pass
                continue
                
            stadtteile_dict[stadtteil] += 1
        
        return stadtteile_dict


    def __beta_tester(self):
        """beta version disclaimer"""
        if self.version is "beta":
            print("Warning: Crawler is still in Beata version. Contact Tim for help.")


    def __warning_bad_data_quality(self):
        """prints warning"""
        print("Warning: The dataquality is terrible! Not complete dataset might obscure your result")
    
