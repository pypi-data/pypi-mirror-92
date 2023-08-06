from collections.abc import Mapping


class BaseExpression:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Str(BaseExpression):
    pass


class Num(BaseExpression):
    pass


class Bool(BaseExpression):
    pass


class Nested(BaseExpression):
    def __init__(self, key, value):
        self.key = key
        self.value = []
        if isinstance(value, BaseExpression):
            self.value = [value]
        if isinstance(value, Mapping):
            for key, value in value.items():
                self.value.append(build_expr_obj(key, value))


class GTE(BaseExpression):
    pass


class LTE(BaseExpression):
    pass


class GT(BaseExpression):
    pass


class LT(BaseExpression):
    pass


class IN(BaseExpression):
    pass


class NE(BaseExpression):
    pass


LOGICALS = {
    'gte': GTE,
    'lte': LTE,
    'lt': LT,
    'gt': GT,
    'in': IN,
    'ne': NE
}


def build_expr_obj(key, value):
    from mjango import models
    build_ins = key.split('__')
    if build_ins[-1] == '':
        raise ValueError('Invalid build in expressions')

    if len(build_ins) == 2 and build_ins[-1] in LOGICALS:
        build_in = build_ins[-1]
        return LOGICALS[build_in](build_ins[0], value)

    if len(build_ins) > 1:
        nested = build_expr_obj('__'.join(build_ins[1:]), value)
        kwargs = {'key': build_ins[0], 'value': nested}
        return Nested(**kwargs)

    if isinstance(value, BaseExpression):
        return Nested(key, value)
    if isinstance(value, models.Model):
        return Str(key, getattr(value, value.pk))
    if isinstance(value, str):
        return Str(key, value)
    if isinstance(value, bool):
        return Bool(key, value)
    if isinstance(value, (int, str, float)):
        return Num(key, value)
    if isinstance(value, Mapping):
        return Nested(key, value)

    raise TypeError(f'unexpected value type, {value.__class__.__name__}')
