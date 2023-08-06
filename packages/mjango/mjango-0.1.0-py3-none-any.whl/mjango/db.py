from mjango import db_settings, exceptions, operators

FILTER = 'filter'
GET = 'get'
CREATE = 'create'
DELETE = 'delete'
UPDATE = 'update'
BATCH_UPDATE = 'batch_update'
COUNT = 'count'


class BaseDB:
    def create(self, **kwargs):
        raise NotImplementedError('create() should be implement')

    def filter(self, query):
        raise NotImplementedError('filter() should be implement')

    def update(self, query, data):
        raise NotImplementedError('update() should be implement')

    def delete(self, query):
        raise NotImplementedError('delete() should be implement')

    def execute(self, query, method_name, slicing=None, **kwargs):
        method = getattr(self, method_name)
        compiled = self.query_compiler.compile(query)
        result = method(compiled, **kwargs)
        if slicing:
            return result[slicing]
        return result


class QueryCompiler:
    def compile_expr(self, exprs):
        return [self.expr_compiler.compile(expr) for expr in exprs]

    def compile(self, query):
        methname = 'compile_' + query.__class__.__name__.lower()
        method = getattr(self, methname, None)
        if not method:
            raise NotImplementedError(f'{methname}() should be implemented')
        return method(query)


class ExprCompiler:
    def compile(self, expr):
        methname = 'compile_' + expr.__class__.__name__.lower()
        method = getattr(self, methname, None)
        if not method:
            raise NotImplementedError(f'{methname}() should be implemented')
        return method(expr)
