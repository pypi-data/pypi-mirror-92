
import datetime

date_past = datetime.datetime.fromisoformat('2019-01-01')
date_now = datetime.datetime.fromisoformat('2020-01-01')
date_future = datetime.datetime.fromisoformat('2021-01-01')



class Test_schema:

    def __init__(self, name = 'test_name'):

        self.credibility = 50
        self.datasource_date_created = date_now
        self.datasource_date_modified = date_now 
        
        self.name = name
        self.domain = 'test.com'

        self.record_type = 'schema:test'
        self.record_id = self.name



    @property
    def email(self):

        name = self.name.replace(' ', '').lower()
        email = name + '@' + self.domain

        return email

    @property
    def url(self):
        url = 'https://' + self.domain

        return url

    @property
    def base(self):

        record = {
            '@type': self.record_type,
            '@id': self.name,
            'schema:name': self.name,
            'schema:url': self.url,
            'schema:email': self.email
        }

        return record

    def base_list(self, qty=3):

        records = []
        for i in range(0, qty):
            name = self.name + str(i)
            records.append(Test_schema(name).base)
        return records
    

    @property
    def metadata(self):

        metadata = {
            'kraken:credibility': self.credibility,
            'kraken:datasource_date_created': self.datasource_date_created,
            'kraken:datasource_date_modified': self.datasource_date_modified

        }

        return metadata


    @property
    def record(self):

        record = {**self.base, **self.metadata}

        return record



    @property
    def complex(self):


        record = self.record

        record['schema:sub_rec'] = Test_schema('sub_rec').base
        
        record['schema:sub_list'] = Test_schema('sub_list').base_list()

        return record


    def krkn_element(self, value):

        if not isinstance(value, list):
            value = [value]

        records = []
        for i in value:
            record = self.metadata
            record['value'] = i
            records.append(record)

        return records


    def krkn(self):

        # transform into krkn record

        new_record = {}

        for i in self.base:
            if i in ['@type', '@id']:
                new_record[i] = self.base[i]
            
            else:
                new_record[i] = self.krkn_element(self.base[i])
            
        return new_record



