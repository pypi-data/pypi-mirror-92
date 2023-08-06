

from kraken_record.kraken_attribute import Kraken_attribute


class Kraken_record:
    '''

    Main api:
    - set: loads schema/json type record
    - get: retrieves dict from record
    - set_attr: set a specific Attribute
    - get_attr: retrieves a specific attribute as attribute class
    - get_attr_record: retrieves a specific attribute as dict 
    - get_attr_best: retrieves best value from attribute (instead of the list)
    - load: load data from source (database for example)
    - dump: dump data to source (database for example)

    Properties:
    - ref_id: returns type/id combination
    - datamap: returns dict of official keys and synonyms


    '''





    def __init__(self):

        self.record_type = None
        self.record_id = None

        self.input_value = None

        self.attributes = {}

        self.sub_records = []




    def __repr__(self):

        return str(self.get())


    def __str__(self):

        return str(self.get())


    def __lt__(self, other):
        
        # Error handling
        if not isinstance(other, Kraken_record):
            return False
        
        # Compare if less or equal
        if not self <= other:
            return False

        # Compare if equal
        if self != other:
            return True

        return False


    def __le__(self, other):

        # Error handling
        if not isinstance(other, Kraken_record):
            return False

        # Compare attributes
        for i in self.attributes:
            value_self = self.get_attr_record(i)
            value_other = other.get_attr_record(i)

            for v in value_self:
                if v not in value_other:
                    print('1')
                    return False

        return True



    def __eq__(self, other):

        # Error handling
        if not isinstance(other, Kraken_record):
            return self

        # Compare attributes
        for i in self.attributes:
            value_self = self.get_attr_record(i)
            value_other = other.get_attr_record(i)

            if value_self != value_other:
                return False


        # Assume equal 
        return True


    def __add__(self, other):

        # Error handling
        if not isinstance(other, Kraken_record):
            return self

        # Initialize new record
        new_kraken_record = Kraken_record()
        new_kraken_record.record_type = self.record_type
        new_kraken_record.record_id = self.record_id

        # Load first record
        for i in self.attributes:
            value = self.get_attr_record(i)
            new_kraken_record.set_attr(i, value)

        new_kraken_record.sub_records += self.sub_records

        # Load second record
        for i in other.attributes:
            value = other.get_attr_record(i)
            new_kraken_record.set_attr(i, value)
        
        new_kraken_record.sub_records += other.sub_records


        # Return new record
        return new_kraken_record


    def get(self):

        record = {}
        record['@type'] = self.record_type
        record['@id'] = self.record_id

        for i in self.attributes:
            record[i] = self.get_attr_record(i)


        return record


    def get_simple(self):

        record = {}
        record['@type'] = self.record_type
        record['@id'] = self.record_id

        for i in self.attributes:
            attrs = self.get_attr(i)
            
            record[i] = []
            for p in attrs:
                value = p.value
                if value not in record[i]:
                    record[i].append(value)
            
            if len(record[i]) == 1 :
                record[i] = record[i][0]


        return record


    def set(self, value):


        # Error handling     
        if not value:
            return   
        
        if not isinstance(value, dict):
            return

        # Assign value
        self.input_value = value
        
        # Clean input data
        self._clean_input_value()

        # Retrieve metadata from input value
        metadata = self._get_metadata_from_input_value()

        # Assign metadata
        if metadata.get('kraken:record_type', None):
            self.record_type = metadata.get('kraken:record_type', None)

        if metadata.get('kraken:record_id', None):
            self.record_id = metadata.get('kraken:record_id', None)


        # Retrieve data from input value
        for i in self.input_value:

            # Skip if metadata
            if i in self.datamap:
                continue

            value = self.input_value.get(i, None)

            # Skip if empty
            if not value:
                continue

            # Combine value and metadata
            value_set = metadata
            value_set['kraken:value'] = value
            self.set_attr(i, value_set)


        # Set record_id
        self._get_record_id()

        return


    def load(self, record):

        # error handling
        if not isinstance(record, dict):
            return

        # Assign metadata
        if record.get('kraken:record_type', None):
            self.record_type = record.get('kraken:record_type', None)

        if record.get('kraken:record_id', None):
            self.record_id = record.get('kraken:record_id', None)        

        # Assign values
        for i in record:
            if i in ['kraken:record_type', 'kraken:record_id']:
                continue

            value = record.get(i, None)
            self.set_attr(i, value)

        return


    def dump(self):

        record = {}

        record['kraken:record_type'] = self.record_type
        record['kraken:record_id'] = self.record_id
        
        for i in self.attributes:
            record[i] = self.get_attr_record(i)

        return record



    @property
    def ref_id(self):

        ref_id = {
            '@type': self.record_type,
            '@id': self.record_id
        }

        return ref_id


    def set_attr(self, attr_name, attr_value):

        clean_attr_name = self._clean_key(attr_name)

        # COnvert to list if not one already
        if not isinstance(attr_value, list):
            attr_value = [attr_value]

        for i in attr_value:

           
            # Case: if sub-schema, create new record instance and link to ref_id
            sub_value = i.get('kraken:value', None)

            if isinstance(sub_value, dict):
                sub_type = sub_value.get('@type', None)
                if sub_type:

                    sub_kr = Kraken_record()
                    sub_kr.set(sub_value)
                    i['kraken:value'] = sub_kr.ref_id

                    # Assign newly created sub records and related sub records to .sub_records
                    self.sub_records.append(sub_kr)
                    self.sub_records += sub_kr.sub_records


            # Initialize new Attribute. 
            new_attribute = Kraken_attribute()
            new_attribute.set(i)

            # Add to list if not already in it. 
            list_attribute = self.attributes.get(clean_attr_name, [])

            if new_attribute not in list_attribute:
                list_attribute.append(new_attribute)
                self.attributes[clean_attr_name] = list_attribute


        return


    def get_attr(self, attr_name):
        # Returns datapoints under attribute in reverse order 

        clean_attr_name = self._clean_key(attr_name)

        list_attribute = self.attributes.get(clean_attr_name, [])

        list_attribute.sort(reverse=True)

        return list_attribute


    def get_attr_record(self, attr_name):
        # return data in attribute as dict instead of class
        attributes = self.get_attr(attr_name)

        records = []
        for i in attributes:
            records.append(i.get())


        return records


    def get_attr_best(self, attr_name):

        records = self.get_attr(attr_name)

        if records:
           return records[0].value

        else:
            return None 


    def _clean_input_value(self):
    

        self._clean_input_value_keys()
        self._clean_input_value_datasource()
            

    def _clean_input_value_keys(self):

        # Error handling
        if self.input_value == None:
            return


        value = self.input_value

        clean_record = {}


        # Clean key names
        for key in value:

            clean_key = self._clean_key(key)
            
            clean_record[clean_key] = value.get(key, None)


        self.input_value = clean_record

        return 


    def _clean_input_value_datasource(self):
        # flatten datasource information if exist

        # Error handling
        if self.input_value == None:
            return

        if not isinstance(self.input_value, dict):
            return

        if not self.input_value.get('kraken:datasource', None):
            return
        
        datasource = self.input_value.get('kraken:datasource', None)

        if not isinstance(datasource, dict):
            return

        for i in datasource:
            if datasource.get(i, None): 
                self.input_value[i] = datasource[i]

        return


    def _clean_key(self, key):

        datamap = self.datamap

        clean_record = {}


        # Clean key names

        clean_key = key
        clean_key = clean_key.lower()
        clean_key = clean_key.strip()

        # Replace by proper synonym
        for i in datamap:
            if clean_key in datamap.get(i, None):
                clean_key = i

        return clean_key


    def _get_metadata_from_input_value(self):
        # Retrieve metadata from input value
        datamap = self.datamap
        metadata = {}

        for i in datamap:
            meta_value = self.input_value.get(i, None)
            if meta_value:
                metadata[i] = meta_value

        return metadata


    def _get_record_id(self):

        if self.record_type == 'schema:webpage':
            self.record_id = self.get_attr_best('schema:url')

        return


    @property
    def datamap(self):

        datamap = {
                'kraken:record_type': [
                    '@type', 'record_type', 'kraken:record_type'],
                'kraken:record_id': [
                    '@id', 'record_id', 'kraken:record_id'],
                'kraken:credibility': [
                    'credibility', 'probability'],
                'kraken:datasource_date_created': [
                    'datasource_date_created', 'datasource_created_date'],
                'kraken:datasource_date_modified': [
                    'datasource_date_modified', 'datasource_modified_date'],
                'kraken:datasource_id': [
                    'datasource_id', 'datasourceid'], 
                'kraken:datasource_name': [
                    'datasource_name', 'datasourcename']
            }

        return datamap