from Crawler import Crawler


class Selector:
    """Offering methods to select relevant Stadtteile based on criterias"""

    def __init__(self):
        """loads everything at initialization"""
        self.my_crawler = Crawler()
        self.__load_cache()
        
    
    def select_by_number(self, modus, anzahl, comparator):
        """
            param: modus: String mit dem modus. z.B. 'kitas' oder 'schulen'
            param: anzahl: Integer mit der Anzahl die max/min enthalten sein soll
            param: comparator: char either 'greater' or 'smaller'
            Returns tupe (dict and a list). Dict keys: stadtteil; Value:Anzahl.
            List only with relevant stadtteile
        """
        # check for correct input 
        self._check_if_input_valid(modus, anzahl, comparator)

        # choose the relevant dict by modus. z.B. schulen_dict
        relevant_dict = self.__select_dict(modus)

        # iterate to get all items matching the paramteter 'anzahl'
        return_dict = dict()
        for key, value in relevant_dict.items():
            if comparator == "greater":
                if value>= anzahl:
                    return_dict[key]= value
            elif comparator == "smaller":
                if value<= anzahl:
                    return_dict[key]= value
            else:
                raise AttributeError("no comparision is beeing made")

        # creatre return_list from keys of return_dict
        return_list = return_dict.keys()
        
        # return tuple
        return (return_dict, return_list)


    def __select_dict(self, modus):
        """returns the corresponding dict matching a string identifier"""
        if modus == "kitas":
            return self.kita_dict
        elif modus == "schulen":
            return self.schulen_dict
        elif modus == "behindertenparkplaetze":
            return self.behindertenparkplatz_dict
        

    def _check_if_input_valid(self, modus, anzahl, comparator):
        """Checks if modus is a valid value and anzahl is in a proper range"""
        valid_modus_values = ["kitas","schulen","behindertenparkplaetze"]
        if modus not in valid_modus_values:
            raise ValueError(modus, "is not accepted. Value must be in", valid_modus_values)

        valid_comparator_values = ["greater","smaller"]
        if comparator not in valid_comparator_values:
            raise ValueError(comparator, "is not accepted. Value must be in", valid_comparator_values)
        # TODO: add anzahl tester
        
    
    def __load_cache(self):
        self.behindertenparkplatz_dict = self.my_crawler.get_behindertenparkplatz_dict()
        self.schulen_dict = self.my_crawler.get_schulen_dict()
        self.kita_dict = self.my_crawler.get_kita_dict()
