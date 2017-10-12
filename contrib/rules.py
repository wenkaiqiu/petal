from models import compatible, Model
from models.interfaces import InterfaceSFPP, InterfaceInternal
from models.protocols import ProtocolVLAN, ProtocolTrunk, ProtocolIP


@compatible(ProtocolIP, ProtocolVLAN, ProtocolTrunk)
class CX310(Model):
    # todo: rj45接口仅用于管理，暂时忽略
    # rj45 = InterfaceRJ45(count=2, downlink=True)

    # todo: 调查uplink&downlink是否有存在必要
    sfpp_10ge = InterfaceSFPP(count=16, speed='10', subcard_number=17, port_number=range(1, 17), uplink=True)
    interface_10ge = InterfaceInternal(count=32, speed='10', subcard_number=range(1, 17), port_number=range(1, 3))
    interface_40ge = InterfaceInternal(count=1, speed='40', subcard_number=18, port_number=1)
    interface_ge = InterfaceInternal(count=2, speed='1', subcard_number=19, port_number=range(1, 3))

    def __init__(self, *args, **kwargs):
        super().__init__(args[0])
        self.slot_id = kwargs['slot_id']  # todo: 检查值存在

    def update_interface(self, **kwargs):
        print("1--------------")
        print(kwargs)
        port_id = kwargs['port_id'].split('/')
        print(port_id)
        interface = self.find_interface(port_id[0])
        interface.ports[int(port_id[1])-1].update({'stack_port': kwargs['stack_port'], 'port_mode': 'stack'})
        print(interface.ports[int(port_id[1])-1])

    def find_interface(self, subcard_id):
        print("2--------------")
        interface =  filter(lambda x: x.subcard_number == int(subcard_id) if type(x.subcard_number) is int else int(
            subcard_id) in x.subcard_number, self.interfaces())
        return list(interface)[0]
