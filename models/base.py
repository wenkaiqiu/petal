from .interfaces import Interface
from .protocols import BaseProtocol, ProtocolNotSupport


class Model:
    def __init__(self, logical_id):
        self.logical_id = logical_id

    def __str__(self):
        return f'{type(self).__name__}'

    @classmethod
    def has(cls, interface):
        return interface in cls.interfaces()

    @classmethod
    def interfaces(cls):
        return set(filter(lambda x: issubclass(x, Interface),
                          map(lambda x: type(getattr(cls, x)),
                              filter(lambda x: not x.startswith('__'),
                                     cls.__dict__.keys()))))


def compatible(*protocols: BaseProtocol):
    def wrap(model: Model):
        name = 'required_interface_set'
        if any(map(lambda p: (hasattr(p, name) and not getattr(p, name).issubset(model.interfaces())),
                   protocols)): raise ProtocolNotSupport()
        setattr(model, 'support_protocols', protocols)
        return model

    return wrap
