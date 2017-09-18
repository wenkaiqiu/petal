from abc import ABCMeta
import logging
from models import compatible, Model, InterfaceRJ45
from models.fileds import InterfaceSFPP

logging.basicConfig(format='%(asctime)s %(filename)-10s %(message)s')
logger = logging.getLogger('rules')
logger.setLevel(logging.DEBUG)


class BaseProtocol(ABCMeta): pass


class ProtocolIP(BaseProtocol):
    a = InterfaceRJ45()
    b = InterfaceRJ45()


class ProtocolVLAN(BaseProtocol):
    a = InterfaceRJ45()
    b = InterfaceRJ45()


class ProtocolStack(BaseProtocol): pass


@compatible(ProtocolIP, ProtocolVLAN, ProtocolStack)
class CX310(Model):
    rj45 = InterfaceRJ45(count=32, downlink=True)
    sfpp = InterfaceSFPP(count=16, uplink=True)


if __name__ == '__main__':
    device = CX310()
    logger.info(dir(device))
    logger.info(device.support_protocols)
    logger.info(device.interface_type_set())
