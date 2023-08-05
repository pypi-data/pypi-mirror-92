from mjango import db_settings, exceptions, operators
from pymongo import MongoClient,  ReturnDocument


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
        return list(self.client.find(query))

    def get(self, query):
        return self.client.find_one(query)

    def create(self, **kwargs):
        self.client.insert_one(kwargs)
        return kwargs

    def delete(self, query):
        self.client.find_one_and_delete(query)

    def update(self, query, data):
        return self.client.find_one_and_update(query, {'$set': data}, return_document=ReturnDocument.AFTER)


class Compiler:
    def compile_and(self, query, cls):
        raise NotImplementedError('compile_and() should be implement')

    def compile_or(self, query, cls):
        raise NotImplementedError('compile_or() should be implement')

    def compile_not(self, query, cls):
        raise NotImplementedError('compile_not() should be implement')

    def create(self, **kwargs):
        raise NotImplementedError('create() should be implement')

    def filter(self, query):
        raise NotImplementedError('filter() should be implement')

    def update(self, query, data):
        raise NotImplementedError('update() should be implement')

    def delete(self, query):
        raise NotImplementedError('delete() should be implement')


class MongoDB(Compiler):
    def __init__(self, collection, settings=None):
        self.db_base = MongoBase(collection, settings)

    def create(self, **kwargs):
        return self.db_base.create(**kwargs)

    def filter(self, query):
        return self.db_base.filter(query)

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

    def compile_and(self, query, cls):
        result = [query.kwargs]
        if query.sub_queries:
            for sub_query in query.sub_queries:
                result.append(cls.compile(sub_query))
        return {
            '$and': result
        }

    def compile_or(self, query, cls):
        result = []
        for key, value in query.kwargs.items():
            result.append({key: value})
        if query.sub_queries:
            for sub_query in query.sub_queries:
                result.append(cls.compile(sub_query))

        return {
            '$or': result
        }

    def compile_empty(self, query, cls):
        return {}
