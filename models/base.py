from models.fileds import Interface


class ProtocolNotSupport(Exception): pass


class Model:
    @classmethod
    def interface_type_set(cls):
        return set(filter(lambda x: issubclass(x, Interface),
                          map(lambda x: type(getattr(cls, x)),
                              filter(lambda x: not x.startswith('__'),
                                     cls.__dict__.keys()))))


def compatible(*protocols):
    def wrap(model):
        name = 'required_interface_set'
        if any(map(lambda p: (hasattr(p, name) and not getattr(p, name).issubset(model.interface_type_set())),
                   protocols)): raise ProtocolNotSupport()
        setattr(model, 'support_protocols', protocols)
        return model

    return wrap


def require(*interface):
    def wrap(protocol):
        protocol.required_interface_set = set(interface)
        return protocol

    return wrap
