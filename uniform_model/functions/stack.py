import logging

from .base import Function
from .utils import render

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('uniform_model.functions.stack')
logger.setLevel(logging.DEBUG)


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
        if not cls.validate(device): return False
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
                if port is None: raise ValueError(f"{port_name} is not in device <{device.id}>")
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
        配置参数, stack_port参数配置
        :param params:
        :return:
        """
        for param in {'domain', 'member_id', 'priority'}:
            # noinspection PyBroadException
            try: setattr(self, param, params[param])
            except Exception: pass

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
        return render('stack', device=self)

    def generate_revoke_conf(self):
        return render('stack_revoke', device=self)
