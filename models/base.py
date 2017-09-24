import logging

from .interfaces import Interface
from .protocols import Protocol, ProtocolNotSupport

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('model_base')
logger.setLevel(logging.DEBUG)

# TODO: Use trie latter for better performance.
__global_register = set()


def _register_model(cls: object, model_id):
    global __global_register
    identifier = f'{cls.__name__}>>{model_id}'
    if identifier in __global_register: raise ValueError(f'model {identifier} already registered.')
    __global_register.add(identifier)
    logger.info(f'register model {identifier} success')


def list_all_registered():
    return __global_register


class ModelType(type):
    def __str__(cls):
        return f'<Model: {cls.__name__}>'

    def __repr__(cls):
        return f'<Model: {cls.__name__}>'


class Model(metaclass=ModelType):
    def __new__(cls, *args, **kwargs):
        _register_model(cls, args[0])
        return cls

    def __init__(self, logical_id):
        self.logical_id = logical_id

    @classmethod
    def has(cls, interface):
        return interface in cls.interfaces()

    @classmethod
    def interfaces(cls):
        return set(filter(lambda x: issubclass(x, Interface),
                          map(lambda x: type(getattr(cls, x)),
                              filter(lambda x: not x.startswith('__'),
                                     cls.__dict__.keys()))))


def compatible(*protocols: Protocol):
    def wrap(model: Model):
        name = 'required_interface_set'
        if any(map(lambda p: (hasattr(p, name) and not getattr(p, name).issubset(model.interfaces())),
                   protocols)): raise ProtocolNotSupport()
        setattr(model, 'support_protocols', protocols)
        return model

    return wrap


class ModelGroup:
    def __init__(self, *args):
        self.group = list(args)

    def __str__(self):
        return f'<Group: {", ".join(map(str, self.group))}>'

    def __repr__(self):
        return f'<Group: {", ".join(map(str, self.group))}>'
