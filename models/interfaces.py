class InterfaceType(type):
    def __str__(cls): return f'<Interface: {cls.__name__}>'

    def __repr__(cls): return f'<Interface: {cls.__name__}>'


class Port:
    pass


class Interface(metaclass=InterfaceType):
    def __init__(self, *args, **kwargs):
        self.bundle = 'count' in kwargs
        self.count = kwargs['count'] if 'count' in kwargs else 1
        self.speed = kwargs['speed'] if 'speed' in kwargs else None
        self.subcard_number = kwargs['subcard_number'] if 'subcard_number' in kwargs else 0  # int or range
        self.port_number = kwargs['port_number'] if 'port_number' in kwargs else 1
        base = self.subcard_number if type(self.subcard_number) == int else self.subcard_number[0]
        len_port_number = self.port_number if type(self.port_number) == int else len(self.port_number)
        self.ports = [{'subcard_number': (base + i // len_port_number), 'port_number': (i % len_port_number + 1)}
                      for i in range(self.count)]


class InterfaceRJ45(Interface):
    pass


class InterfaceSFPP(Interface):
    pass


class InterfaceInternal(Interface):
    pass
