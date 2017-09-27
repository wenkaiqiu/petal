from models import compatible, Model
from models.interfaces import InterfaceSFPP, InterfaceRJ45
from models.protocols import ProtocolVLAN, ProtocolTrunk, ProtocolIP


@compatible(ProtocolIP, ProtocolVLAN, ProtocolTrunk, interface_type='InterfaceRJ45')
@compatible(ProtocolIP, ProtocolVLAN, ProtocolTrunk, interface_type='InterfaceSFPP')
class CX310(Model):
    rj45 = InterfaceRJ45(count=32, downlink=True)
    sfpp = InterfaceSFPP(count=16, uplink=True)

