class RuleBase:
    def apply(self, a, b): raise NotImplementedError()


class Statement(RuleBase):
    def __init__(self, statement):
        self.statement = statement

    def apply(self, a, b): return self.statement


class When(RuleBase):
    def __init__(self, notation: str, sub_a: RuleBase, sub_b: RuleBase):
        self.notation = notation
        self.sub_a = sub_a
        self.sub_b = sub_b

    def apply(self, a, b):
        if eval(self.notation): return self.sub_a.apply(a, b)
        return self.sub_b.apply(a, b)


class Need(RuleBase):
    def __init__(self, notation: str):
        self.notation = notation

    def apply(self, a, b):
        return eval(self.notation)


class Entity:
    def __init__(self, name, attrs=(), funcs=(), required=False):
        self.name = name
        self.attrs = attrs
        self.funcs = funcs
        self.required = required

    def validate(self, obj):
        return all((
            obj or (self.required and not obj),
            all(attr in dir(obj) for attr in self.attrs),
            # TODO: more precise checks
            all(func in dir(obj) for func in self.funcs),
        ))
