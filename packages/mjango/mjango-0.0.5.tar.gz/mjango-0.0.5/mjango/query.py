from mjango import operators
from functools import reduce


class BaseIterable:
    def __init__(self, queryset):
        self.queryset = queryset


class ModelIterable(BaseIterable):
    def __iter__(self):
        db = self.queryset.db
        query = self.queryset.query
        params = query or operators.EMPTY()
        compiler = params.get_compiler(db, self.queryset.method)
        result = compiler.execute()
        for item in result:
            yield(self.queryset.model(item))


class ValuesIterable(BaseIterable):
    def __iter__(self):
        db = self.queryset.db
        query = self.queryset.query
        params = query or operators.EMPTY()
        compiler = params.get_compiler(db, self.queryset.method)
        result = compiler.execute()
        return iter(result)


class QuerySet:
    def __init__(self, model, method=None, query=None, iter_class=None):
        self.model = model
        self._query = query
        self.method = method
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

    def __getitem__(self, index):
        self._fetch_all()
        return self._cached_result[index]

    def _make_query(self, *query, **kwargs):
        kwargs_q = operators.AND(**kwargs)
        query_queue = [*query, kwargs_q]
        if self._query:
            query_queue.append(self._query)
        query = reduce(lambda x, y: x & y, query_queue)
        return query

    def _clone(self, query, method=None, iter_class=None):
        if not method:
            method = self.method
        queryset = self.__class__(
            self.model, method=method, query=query, iter_class=iter_class)
        return queryset

    def filter(self, *query, **kwargs):
        query = self._make_query(*query, **kwargs)
        return self._clone(query, method='filter')

    def values(self):
        return self._clone(self._query, iter_class=ValuesIterable)

    def get(self, *query, **kwargs):
        query = self._make_query(*query, **kwargs)
        compiler = query.get_compiler(self.db, 'get')
        return self.model(compiler.execute())

    def create(self, **kwargs):
        result = self.db.create(**kwargs)
        return self.model(result)

    def all(self):
        return self._clone(None, method='filter')
