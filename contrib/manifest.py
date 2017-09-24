import logging

from contrib.rules import CX310, ProtocolTrunk, ProtocolIP
from models.actions import link, group
from models.base import list_all_registered

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('manifest')
logger.setLevel(logging.DEBUG)

cx310_1 = CX310('1321')
cx310_2 = CX310('1322')
cx310_3 = CX310('1323')

link(cx310_1, cx310_2, ProtocolTrunk)
link(group(cx310_1, cx310_2), cx310_3, ProtocolIP)
logger.info(ProtocolTrunk.interfaces())
logger.info(ProtocolTrunk.interfaces())
logger.info(list_all_registered())
logger.info(CX310.__repr__())
