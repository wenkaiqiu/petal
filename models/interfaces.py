class InterfaceType(type):
    def __str__(cls): return f'<Interface: {cls.__name__}>'

    def __repr__(cls): return f'<Interface: {cls.__name__}>'


class Interface(metaclass=InterfaceType):
    def __init__(self, *args, **kwargs):
        self.bundle = 'count' in kwargs
        self.base = {}
        self.attr = {}
        if kwargs.get('name'):
            self.base['name'] = kwargs['name']
        if kwargs.get('speed'):
            self.base['speed'] = kwargs['speeed']
        if kwargs.get('subcard_number'):
            self.base['subcard_number'] = kwargs['subcard_number']
        if kwargs.get('port_number'):
            self.base['port_number'] = kwargs['port_number']

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


class InterfaceInternal(Interface): pass


class AttrNotExist(Exception): pass
