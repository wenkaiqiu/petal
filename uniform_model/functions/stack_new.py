import logging
from .utils import render

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('uniform_model.functions.stack_new')
logger.setLevel(logging.DEBUG)


class Rule:
    def __init__(self, *args):
        pass


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


class FunctionNew:
    def generate_conf(self): return render('stack', **self.entities)

    def generate_revoke_conf(self): return render('stack_revoke', **self.entities)

    name = str()
    entities = dict()
    inner_rules = tuple()
    intra_rules = tuple()
    vals = set()
    __entities = dict(this=dict())

    def __init__(self, *args, **kwargs):
        # entity check
        if not all((
                # TODO: check not required
                all(name in kwargs and entity.validate(kwargs[name])
                    for name, entity in self.entities
                    if entity.required),
                all(val in kwargs for val in self.vals)
        )): raise Exception()

        # fill vals
        for key in self.vals: self.__entities['this'][key] = kwargs[key]


class FunctionStack(FunctionNew):
    name = "stack"
    vals = {'domain_id', 'priority', 'port_id', 'physical_port'}
    entities = {
        'device': Entity('device', ('interface', 'slot_id'), ()),
    }
    inner_rules = (
    )
    intra_rules = (
        Rule()
    )

    def __init__(self, *args, **kwargs):
        super(FunctionStack, self).__init__(*args, **kwargs)
        self.__entities['this']['member_id'] = kwargs['device'].slot_id
        self.__entities['this']['port_id'] = kwargs['port_id']
        self.__entities['this']['port_name'] = kwargs["physical_port"]