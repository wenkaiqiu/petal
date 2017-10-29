import logging
from collections import Counter
from functools import reduce
from models.interfaces import Interface

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('functions')
logger.setLevel(logging.DEBUG)


class OperableTrait:
    @classmethod
    def op(cls, *arith_list, **kwargs): raise NotImplemented()


class FunctionType(type):
    def __str__(cls):
        return f'<Protocol: {cls.__name__}>'


class Function(OperableTrait, metaclass=FunctionType):
    dependencies = []

    @classmethod
    def validate(cls, device):
        """
        自定义协议和模型检查流程，在接口检查后自动调用
        :return: 检查通过返回真，否则 raise对应错误(推荐) 或者 返回False
        """
        try:
            if not cls._check_protocol_support(device):
                raise ProtocolNotSupport(f"device {device.id} not support FunctionStack")
            if not cls._check_dependencies(device):
                return False
        except ProtocolNotSupport as e:
            print(e)
            return False
        return True

    @classmethod
    def _check_protocol_support(cls, device):
        return cls.name in device.support_functions

    @classmethod
    def _check_dependencies(cls, device):
        for dependency in cls.dependencies:
            if not getattr(device, dependency).enable:
                return False
        return True

    def generate_conf(self):
        pass


class FunctionIP(Function):
    attrs = ['bootproto', 'broadcast', 'ipaddr', 'netmask', 'network']

    @classmethod
    def op(cls, arith_list):
        print(f'op on {arith_list}')


class FunctionVLAN(Function):
    @classmethod
    def op(cls, arith_list):
        print(f'op on {arith_list}')


class FunctionTrunk(Function):
    @classmethod
    def op(cls, arith_list):
        print(f'op on {arith_list}')


class FunctionStack(Function):
    name = "stack"
    dependencies = []

    @classmethod
    def op(cls, *arith_list, **kwargs):
        """
        执行配置操作
        :param arith_list: 待配置设备列表，注：目前仅涉及配置单设备情况，见actions里的处理
        :param kwargs:
        :return:
        """
        logger.info(f"running <FunctionStack> op")
        device = arith_list[0]
        # 检验依赖关系
        if not cls.validate(device):
            return False
        device_stack = getattr(device, cls.name)
        # print("--------op-------------")
        # print(device_stack.__dict__)
        # print(dict(filter(lambda k: not k[0].startswith("__"), device.__dict__.items())))
        logger.info(f'param in <FunctionStack>: {kwargs}')

        # 设置设备的stack属性
        device_stack.init_attrs(device)
        device_stack.set_attrs(kwargs)
        # 设置interface属性
        if "stack_port" in kwargs:
            for item in kwargs["stack_port"]:
                port_id = item["port_id"]
                port_name = item["physical_port"]
                port = device.interfaces.get(port_name, None)
                if port is None:
                    raise ValueError(f"{port_name} is not in device <{device.id}>")
                device_stack.set_stack_port(port_id, port)
                port.set_attr("mode", "stack")
        device_stack.enable = True
        # print(device_stack.__dict__)
        return True

    @classmethod
    def validate(cls, device):
        tag = super().validate(device)
        return tag

    def init_attrs(self, device):
        self.member_id = device.slot_id

    def set_attrs(self, params):
        """
        配置参数, stack_port参赌配置
        :param params:
        :return:
        """
        for item in params:
            if item == "domain_id":
                self.domain_id = params[item]
            elif item == "member_id":
                self.member_id = params[item]
            elif item == "priority":
                self.priority = params[item]

    def set_stack_port(self, port_id, physical_port):
        """
        添加物理端口到stack端口
        :param port_id: string类型
        :param physical_port:
        :return:
        """
        if port_id in self.stack_port:
            self.stack_port[port_id].append(physical_port)
        else:
            self.stack_port.update({port_id: [physical_port]})

    def __init__(self):
        self.enable = False
        self.domain_id = None
        self.member_id = None
        self.priority = 100
        self.stack_port = {}

    def generate_conf(self):
        output = []
        # todo: 是否需要进行检查？
        output.append("stack")
        output.append("stack member " + str(self.member_id) + " priority " + str(self.priority))
        output.append("stack member " + str(self.member_id) + " domain " + str(self.domain_id))
        output.append("quit")
        output.append("commit")
        # 创建堆叠端口
        output.append("system-view")
        for port_id in self.stack_port:
            output.append("interface stack-port " + str(self.member_id) + "/" + str(port_id))
        # 配置业务口为堆叠物理端口，将业务口加入堆叠端口
        for port_id, interface in self.stack_port.items():
            # print("interface "+repr(interface)[1:-1])
            output.append("interface "+repr(interface)[1:-1])
            output.append("port mode stack")
            output.append("stack-port "+str(self.member_id) + "/" + str(port_id))
            output.append("commit")
            output.append("quit")
        return output


class ProtocolNotSupport(Exception):
    pass
