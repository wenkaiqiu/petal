class InterfaceType(type):
    def __str__(cls): return f'<Interface: {cls.__name__}>'

    def __repr__(cls): return f'<Interface: {cls.__name__}>'


class Interface(metaclass=InterfaceType):
    def __init__(self, *args, **kwargs): pass


class InterfaceRJ45(Interface): pass


class InterfaceSFPP(Interface): pass
