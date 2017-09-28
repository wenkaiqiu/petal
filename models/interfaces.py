class InterfaceType(type):
    def __str__(cls): return f'<Interface: {cls.__name__}>'

    def __repr__(cls): return f'<Interface: {cls.__name__}>'


class Interface(metaclass=InterfaceType):
    def __init__(self, *args, **kwargs):
        self.bundle = 'count' in kwargs
        meta = {}
        self.base = {}
        self.attr = {}
        if meta.get('name'):
            self.base['name'] = meta['name']
        if meta.get('speed'):
            self.base['speed'] = meta['speeed']
        if meta.get('subcard_number'):
            self.base['subcard_number'] = meta['subcard_number']
        if meta.get('port_number'):
            self.base['port_number'] = meta['port_number']

    def getattr(self, attr_name):
        if not (attr_name in self.attr.keys()):
            raise AttrNotExist
        return self.attr[attr_name].get_value()

    def setattr(self, attr_name, value):
        if not (attr_name in self.attr.keys()):
            raise AttrNotExist
        self.attr[attr_name].set_value(value)

    def init_attr(self, attr_name, field=None):
        self.attr[attr_name] = field
        print(self.getattr(attr_name))


class InterfaceRJ45(Interface): pass


class InterfaceSFPP(Interface): pass


class InterfaceInternal(Interface): pass


class AttrNotExist(Exception): pass
