from pymongo import MongoClient,  ReturnDocument
from mjango import db, exceptions
from mjango.mongodb.compilers import QueryCompiler


class MongoBase:
    def __init__(self, collection, settings=None):
        self.collection = collection
        self.settings = settings or db_settings

    @property
    def db_host(self):
        if not self.settings.db_host:
            raise exceptions.SettingsError
        return self.settings.db_host

    @property
    def db_name(self):
        return self.settings.db_name

    @property
    def client(self):
        return MongoClient(self.db_host)[self.db_name][self.collection]

    def filter(self, query):
        return self.client.find(query)

    def get(self, query):
        return self.client.find_one(query)

    def create(self, **kwargs):
        self.client.insert_one(kwargs)
        return kwargs

    def delete(self, query):
        self.client.find_one_and_delete(query)

    def update(self, query, data):
        return self.client.find_one_and_update(query, {'$set': data}, return_document=ReturnDocument.AFTER)

    def count(self, query):
        return self.client.count_documents(query)

    def batch_update(self, query, data):
        return self.client.update_many(query, {'$set': data})


class MongoDB(db.BaseDB):
    query_compiler = QueryCompiler()

    def __init__(self, collection, settings=None):
        self.db_base = MongoBase(collection, settings)

    def create(self, **kwargs):
        return self.db_base.create(**kwargs)

    def filter(self, query):
        return self.db_base.filter(query)

    def count(self, query):
        return self.db_base.count(query)

    def update(self, query, data):
        return self.db_base.update(query, data=data)

    def delete(self, query):
        return self.db_base.delete(query)

    def all(self):
        return self.db_base.filter({})

    def get(self, query):
        result = self.db_base.get(query)
        if not result:
            raise exceptions.InstanceNotFound
        return result

    def batch_update(self, query, data):
        result = self.db_base.batch_update(query, data=data)
        return {'count': result.matched_count, 'data': data}
