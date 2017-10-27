# from models import compatible, Model
# from models.interfaces import InterfaceSFPP, InterfaceInternal
# from models.functions import FunctionVLAN, FunctionTrunk, FunctionIP, FunctionStack
# from models.utils import parse_interface_id
#
#
# @compatible(FunctionIP, FunctionVLAN, FunctionTrunk, FunctionStack)
# class CX310(Model):
#     # todo: 该设备中rj45接口仅用于管理，暂时忽略
#     # rj45 = InterfaceRJ45(count=2, downlink=True)
#
#     # todo: 调查uplink&downlink是否有存在必要
#     """
#     描述某一类型的接口，一类接口可能有多个物理或逻辑接口
#     """
#     sfpp_10ge = InterfaceSFPP(count=16, speed='10', subcard_number=17, port_number=range(1, 17), uplink=True)
#     interface_10ge = InterfaceInternal(count=32, speed='10', subcard_number=range(1, 17), port_number=range(1, 3))
#     interface_40ge = InterfaceInternal(count=1, speed='40', subcard_number=18, port_number=1)
#     interface_ge = InterfaceInternal(count=2, speed='1', subcard_number=19, port_number=range(1, 3))
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(args[0])
#         self.slot_id = kwargs['slot_id'] if 'slot_id' in kwargs else None
#         if self.slot_id is None:
#             raise ValueError("slot_id is need for init of <CX310>")
#
#     def update_attr_to_interface(self, **kwargs):
#         # print(kwargs)
#         interface_id = parse_interface_id(kwargs['interface_id'])
#         interface = self._get_interface(**interface_id)
#         interface.update({'stack_port': kwargs['stack_port'], 'port_mode': 'stack'})
#         print(interface)
#
#     def _get_interface(self, subcard_number, port_number):
#         """
#         依靠`subcard_number`和`port_number`获取物理或逻辑接口
#         :param subcard_number:
#         :param port_number:
#         :return:
#         """
#         print(subcard_number, port_number)
#         interface = filter(lambda x: x is not None,
#                            map(lambda y: y.get_interface(subcard_number, port_number), self.interfaces()))
#         return next(interface)
