# import logging
#
# from contrib.rules import CX310, FunctionIP
# from models.actions import op
# from models.models import list_all_registered
# from models.functions import FunctionStack
#
# logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
# logger = logging.getLogger('manifest')
# logger.setLevel(logging.DEBUG)
#
# cx310_1 = CX310('1321', slot_id='2')
# cx310_2 = CX310('1322', slot_id='3')
# cx310_3 = CX310('1323', slot_id='2')
#
# stack_params = [
#     {
#         'domain_id': 10,
#         'member_id': 2,
#         'priority': 150,
#         'stack_port': [1],
#         'interface': [['18/1']]
#     },
#     {
#         'domain_id': 10,
#         'member_id': 3,
#         'priority': 150,
#         'stack_port': [1],
#         'interface': [['18/1']]
#     }
# ]
#
# op(FunctionStack, cx310_1, cx310_2, params=stack_params)
# # op(ProtocolTrunk, cx310_1, cx310_2, )
# # op(ProtocolIP, group(cx310_1, cx310_2), cx310_3)
# # op(ProtocolIP, cx310_3)
# # logger.info(ProtocolTrunk.interfaces())
# # logger.info(ProtocolStack.interfaces())
# logger.info(f'registered device: {list_all_registered()}')
# logger.info(f'CX310 registered interface: {cx310_1.interfaces()}')
# logger.info(f'CX310 registered interface type: {cx310_1.interface_types()}')
