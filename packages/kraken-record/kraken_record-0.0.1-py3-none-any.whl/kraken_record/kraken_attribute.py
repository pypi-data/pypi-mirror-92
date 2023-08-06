




class Kraken_attribute:
    def __init__(self, name = None, value = None):

        self.name = None
        self.value = None
        self.credibility = None
        self.source_created_date = None
        self.source_modified_date = None
        self.date_created = None
        self.date_modified = None


        self.attr_list = [
            'value', 
            'credibility', 
            'datasource_date_created', 
            'datasource_date_modified', 
            'datasource_name',
            'datasource_id',
            'datasource_record_id',
            'date_created',
            'date_modified'
            ]


        # Assign name if one
        if name:
            self.name = name


        # assign value if exist
        if value: 
            self.set(value)


    def __repr__(self):

        return str(self.get())


    def __str__(self):

        return str(self.get())


    def __lt__(self, other):

        for i in ['credibility', 'datasource_date_created', 'datasource_date_modified']:

            self_value = getattr(self, i, None)
            other_value = getattr(other, i, None)

            # Continue to next if blank
            if not self_value and not other_value:
                continue

            if self_value and not other_value:
                return False

            if not self_value and other_value:
                return True

            if self_value < other_value:
                return True
        
        return False


    def __eq__(self, other):

        for i in self.attr_list:

            if getattr(self, i, None) != getattr(other, i,  None):
                
                return False

        return True

    def __gt__(self, other):

        if not self < other and self != other:
            return True
        
        else:
            return False

    def __le__(self, other):

        if self < other or self == other:
            return True
        else:
            return False

    def __ge__(self, other):

        if self > other or self == other:
            return True
        else:
            return False

    def __add__(self, other):

        # Keep best attribute
        if self >= other:
            best_attribute = self
        else:
            best_attribute = other


       
    


    def get(self):

        record = {}

        for attr_name in self.attr_list:
            if getattr(self, attr_name, None): 

                record[attr_name] = getattr(self, attr_name, None)

        return record



    def set(self, value):

        # If value is dict, then parse dict into metadata
        if isinstance(value, dict):

            for attr_name in value:

                clean_name = attr_name.replace('kraken:', '')

                attr_value = value.get(attr_name, None)

                if attr_value:
                    setattr(self, clean_name, attr_value)


        # If not dict, assign as value
        else:
            self.value = value


        # Inspect schema validity
        self._schema_check()


        return






    def _schema_check(self):

        self._schema_check_credibility()



    def _schema_check_credibility(self):

        # Exit if None
        if self.credibility == None:
            return


        # Check if int
        if not isinstance(self.credibility, int):
            try:
                self.credibility = int(self.credibility)
            except:
                self.credibility = None

        # Check if between 0 and 100
        if self.credibility < 0 or self.credibility > 100:
            self.credibility = None

        return