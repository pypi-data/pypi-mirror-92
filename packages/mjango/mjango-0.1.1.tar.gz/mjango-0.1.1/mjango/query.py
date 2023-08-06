from mjango import operators, db, exceptions
from functools import reduce


class BaseIterable:
    def __init__(self, queryset):
        self.queryset = queryset


class ModelIterable(BaseIterable):
    def __iter__(self):
        db = self.queryset.db
        query = self.queryset.query
        method = self.queryset.method
        slicing = self.queryset.slicing
        params = query or operators.EMPTY()
        result = db.execute(query, method, slicing=slicing)
        for item in result:
            yield(self.queryset.model(item))


class ValuesIterable(BaseIterable):
    def __iter__(self):
        db = self.queryset.db
        query = self.queryset.query
        params = query or operators.EMPTY()
        slicing = self.queryset.slicing
        result = db.execute(query, method, slicing=slicing)
        return iter(result)


class QuerySet:
    def __init__(self, model, method=None, query=None, slicing=None, iter_class=None):
        self.model = model
        self._query = query
        self.method = method
        self.slicing = slicing
        self._cached_result = None
        self._iter_class = iter_class or ModelIterable

    @property
    def db(self):
        return self.model.db

    @property
    def query(self):
        return self._query

    def _fetch_all(self):
        if self._cached_result is None:
            self._cached_result = list(self._iter_class(self))

    def __iter__(self):
        self._fetch_all()
        return iter(self._cached_result)

    def __getitem__(self, slicing):
        query = self.query.copy()
        return self._clone(query, method=self.method, iter_class=self._iter_class, slicing=slicing)

    def _make_query(self, *query, **kwargs):
        kwargs_q = operators.AND(**kwargs)
        query_queue = [*query, kwargs_q]
        if self._query:
            query_queue.append(self._query)
        query = reduce(lambda x, y: x & y, query_queue)
        return query.copy()

    def _clone(self, query, method=None, iter_class=None, slicing=None):
        if not method:
            method = self.method
        queryset = self.__class__(
            self.model, method=method, query=query, iter_class=iter_class, slicing=slicing)
        return queryset

    def filter(self, *query, **kwargs):
        if self.slicing:
            raise exceptions.QueryError(
                'not able to filter with sliced queryset')
        query = self._make_query(*query, **kwargs)
        return self._clone(query, method=db.FILTER)

    def values(self):
        return self._clone(self._query, iter_class=ValuesIterable)

    def get(self, *query, **kwargs):
        query = self._make_query(*query, **kwargs)
        result = self.db.execute(query, db.GET)
        return self.model()

    def create(self, **kwargs):
        if not self.query:
            raise exceptions.QueryError(
                'queryset does not support create() after first query')
        result = self.db.create(**kwargs)
        return self.model(result)

    def update(self, **kwargs):
        if not self.query:
            raise exceptions.QueryError(
                'queryset does not support update() before first query')
        result = self.db.execute(
            self.query, db.BATCH_UPDATE, data=kwargs)
        return result

    def count(self):
        return self.db.execute(self.query, db.COUNT)

    def all(self):
        if self.query:
            raise expcetions.QueryError(
                'queryset does not support all() after first query')
        return self._clone(operators.EMPTY(), db.FILTER)
