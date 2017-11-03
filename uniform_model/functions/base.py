from uniform_model.functions.utils import render


class FunctionNew:
    def generate_conf(self): return render(self.name, **self._entities)

    def generate_revoke_conf(self): return render(f'{self.name}_revoke', **self._entities)

    name = str()
    entities = dict()
    inner_rules = tuple()
    intra_rules = tuple()
    vals = set()

    def __init__(self, *args, **kwargs):
        self.tag = False
        self._entities = dict(this=dict())  # 用于存放属性
        # entity check, entity可用于推断缺失属性
        if not all((
                # TODO: check not required
                all(name in kwargs and entity.validate(kwargs[name])
                    for name, entity in self.entities.items()
                    if entity.required),
        )): raise Exception()
        # 推断缺失属性
        kwargs = self._infer_value(**kwargs)
        # val check
        if not all(val in kwargs for val in self.vals if self.vals[val]): raise Exception()

        # fill vals
        for key in self.vals: self._entities['this'][key] = kwargs[key]
        if not (self._inner_check()): raise Exception('内部检查失败')

    def _infer_value(self, **kwargs): pass

    def _inner_check(self):
        # inner check
        # print("_inner_check")
        # for rule in self.inner_rules:
        #     print(rule.apply(self, None))
        return all(rule.apply(self, None) for rule in self.inner_rules)

    def intra_check(self, other):
        return all(rule.apply(self, other) for rule in self.intra_rules)

    def __getattr__(self, name):
        try: return self.__dict__[name]
        except KeyError: return self._entities['this'].get(name)