import logging
from models import compatible, Model, InterfaceRJ45
from models.fileds import InterfaceSFPP

logging.basicConfig(format='%(asctime)s %(filename)-10s %(message)s')
logger = logging.getLogger('rules')
logger.setLevel(logging.DEBUG)


class BaseProtocol:
    def __str__(self):
        return f'{type(self).__name__}'


class ProtocolIP(BaseProtocol):
    a = InterfaceRJ45()
    b = InterfaceRJ45()


class ProtocolVLAN(BaseProtocol):
    a = ProtocolIP()
    b = ProtocolIP()


class ProtocolStack(BaseProtocol): pass


@compatible(ProtocolIP, ProtocolVLAN, ProtocolStack)
class CX310(Model):
    rj45 = InterfaceRJ45(count=32, downlink=True)
    sfpp = InterfaceSFPP(count=16, uplink=True)
