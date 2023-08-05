import requests
from mjango import db_settings, db
from mjango.manager import Manager
from mjango.operators import AND
import copy


class ModelBase(type):
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__

        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        meta_attr = attrs.pop('Meta', None)
        collection = meta_attr.collection
        new_class = super_new(cls, name, bases, attrs)

        meta = meta_attr or getattr(new_class, 'Meta', None)
        db_class = getattr(meta, 'db_class', db.MongoDB)
        settings = getattr(meta, 'settings', db_settings)
        new_class.add_to_class('_meta', meta)
        new_class.add_to_class('db', db_class(collection, settings))
        new_class.add_to_class('_collection', collection)
        new_class.add_to_class('objects', Manager(new_class))
        new_class.add_to_class('pk', getattr(meta, 'default_pk', '_id'))

        return new_class

    def add_to_class(cls, name, attr):
        setattr(cls, name, attr)


class Model(metaclass=ModelBase):
    class Meta:
        db_class = db.MongoDB
        settings = db_settings

    def __init__(self, data):
        self._data = data

    def __getattr__(self, key):
        return self._data[key]

    def __setattr__(self, name, value):
        _setattr = super().__setattr__
        if name not in self.__dict__ and not name.startswith('_'):
            self._save(name, value)
        else:
            _setattr(name, value)

    def _save(self, key, value):
        self._data[key] = value

    def save(self):
        kwargs = {self.pk: getattr(self, self.pk)}
        query = AND(**kwargs)
        compiler = query.get_compiler(self.db, method='update')
        return compiler.execute(data=self._data)

    def delete(self):
        kwargs = {self.pk: getattr(self, self.pk)}
        query = AND(**kwargs)
	compiler = query.get_compiler(self.db, method='delete')
        compiler.execute()
        del self._data[self.pk]

    def to_json(self):
        return copy.deepcopy(self._data)
