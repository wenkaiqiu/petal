import logging

from contrib.rules import CX310, ProtocolTrunk, ProtocolIP
from models.actions import link, group, op
from models.base import list_all_registered

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('manifest')
logger.setLevel(logging.DEBUG)

cx310_1 = CX310('1321')
cx310_2 = CX310('1322')
cx310_3 = CX310('1323')

op(ProtocolTrunk, cx310_1, cx310_2, )
op(ProtocolIP, group(cx310_1, cx310_2), cx310_3)
logger.info(ProtocolTrunk.interfaces())
logger.info(ProtocolTrunk.interfaces())
logger.info(f'registered device: {list_all_registered()}')
