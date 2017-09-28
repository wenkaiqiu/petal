from models import compatible, Model
from models.base import register_interface
from models.interfaces import *
from models.protocols import ProtocolVLAN, ProtocolTrunk, ProtocolIP

CX310_port_description = [
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


@compatible(ProtocolIP, ProtocolVLAN, ProtocolTrunk, interface_type='InterfaceRJ45')
@compatible(ProtocolIP, ProtocolVLAN, ProtocolTrunk, interface_type='InterfaceSFPP')
@register_interface(CX310_port_description)
class CX310(Model):
    rj45 = InterfaceRJ45(count=32, uplink=True)
    sfpp = InterfaceSFPP(count=16, uplink=True)

    def __init__(self, logical_id, slot_id):
        print("ccccccc")
        super().__init__(logical_id)
        print("ccccccc")
        print(type(self.interface))
        print(__class__.interface)
        self.slot_id = slot_id
