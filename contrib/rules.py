from models import compatible, Model
from models.interfaces import *
from models.protocols import ProtocolVLAN, ProtocolTrunk, ProtocolIP


@compatible(ProtocolIP, ProtocolVLAN, ProtocolTrunk, interface_type='InterfaceRJ45')
@compatible(ProtocolIP, ProtocolVLAN, ProtocolTrunk, interface_type='InterfaceSFPP')
class CX310(Model):
    _port_description = [
        {
            'type': 'InterfaceRJ45',
            'name': '串口',
            'num': 2
        },
        {
            'type': 'InterfaceSFPP',
            'name': '10GE光口',
            'speed': '10GE',
            'num': 16,
            'subcard_number': range(17, 18),
            'port_number': range(1, 17)
        },
        {
            'type': 'InterfaceInternal',
            'name': '10GE接口',
            'speed': '10GE',
            'num': 32,
            'subcard_number': range(1, 17),
            'port_number': range(1, 3)
        },
        {
            'type': 'InterfaceInternal',
            'name': '40GE接口',
            'speed': '40GE',
            'num': 1,
            'subcard_number': range(18, 19),
            'port_number': range(1, 2)
        },
        {
            'type': 'InterfaceInternal',
            'name': 'GE接口',
            'speed': 'GE',
            'num': 2,
            'subcard_number': range(19, 20),
            'port_number': range(1, 3)
        }
    ]

    def __new__(cls, *args, **kwargs):
        super().__new__(cls, args, kwargs)
        cls.interface = []
        for item in cls._port_description:
            if item.get('subcard_number'):
                len_port = len(item['port_number'])
                for i in range(item["num"]):
                    index_1 = i // len_port
                    index_2 = i % len_port
                    temp = item.copy()
                    temp['subcard_number'] = item['subcard_number'][index_1]
                    temp['port_number'] = item['port_number'][index_2]
                    cls.interface.append(eval(item['type'] + f"({temp})"))
            else:
                for i in range(item["num"]):
                    temp = item.copy()
                    cls.interface.append(eval(item['type'] + f"({temp})"))

    rj45 = InterfaceRJ45(count=32, downlink=True)
    sfpp = InterfaceSFPP(count=16, uplink=True)

    def __init__(self, logical_id, slot_id):
        super().__init__(logical_id)
        self.slot_id = slot_id
