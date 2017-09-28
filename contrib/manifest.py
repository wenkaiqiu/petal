import logging

from contrib.rules import CX310, ProtocolTrunk, ProtocolIP
from models.actions import group, op
from models.base import list_all_registered
from models.interfaces import InterfaceRJ45, InterfaceSFPP

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('manifest')
logger.setLevel(logging.DEBUG)

cx310_1 = CX310('1321')
cx310_2 = CX310('1322')
cx310_3 = CX310('1323')

op(ProtocolTrunk, cx310_1, cx310_2, )
op(ProtocolIP, group(cx310_1, cx310_2), cx310_3)
# logger.info(ProtocolTrunk.interfaces())
# logger.info(ProtocolTrunk.interfaces())
logger.info(f'registered device: {list_all_registered()}')
logger.info(f'<CX310> registered Interface number: {len(cx310_1.interfaces())}')
logger.info(f'<CX310> registered Interface: {cx310_1.interfaces()}')
logger.info(f'<InterfaceRJ45> in <CX310> has base '
            f'<{list(filter(lambda x: type(x)==InterfaceRJ45,cx310_1.interfaces()))[0].base}>')
logger.info(f'<InterfaceRJ45> in <CX310> has attrs '
            f'<{list(filter(lambda x: type(x)==InterfaceSFPP,cx310_1.interfaces()))[0].attr.keys()}>')
logger.info(f'<InterfaceSFPP> in <CX310> has base '
            f'<{list(filter(lambda x: type(x)==InterfaceSFPP,cx310_1.interfaces()))[0].base}>')
logger.info(f'<InterfaceSFPP> in <CX310> has attrs '
            f'<{list(filter(lambda x: type(x)==InterfaceSFPP,cx310_1.interfaces()))[0].attr.keys()}>')
# logger.info(f'<InterfaceSFPP> in <CX310> has attrs <{CX310.sfpp.attr}>')
