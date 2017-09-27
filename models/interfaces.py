class InterfaceType(type):
    def __str__(cls): return f'<Interface: {cls.__name__}>'

    def __repr__(cls): return f'<Interface: {cls.__name__}>'


class Interface(metaclass=InterfaceType):
    def __init__(self, *args, **kwargs):
        self.bundle = 'count' in kwargs
        self.attr = {}

    def getattr(self, attr_name):
        if not (attr_name in self.attr.keys()):
            raise AttrNotExist
        return self.attr[attr_name]

    def setattr(self, attr_name, value):
        if not (attr_name in self.attr.keys()):
            raise AttrNotExist
        self.attr[attr_name] = value

    def init_attr(self, attr_name, default=""):
        self.attr[attr_name] = default


class InterfaceRJ45(Interface): pass


class InterfaceSFPP(Interface): pass


class AttrNotExist(Exception): pass
