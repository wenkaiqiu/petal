import logging
from collections import Counter
from functools import reduce
from models.interfaces import Interface

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('protocols')
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
    def validate(cls, devices):
        """
        自定义协议和模型检查流程，在接口检查后自动调用
        :return: 检查通过返回真，否则 raise对应错误(推荐) 或者 返回False
        """
        return True

    @classmethod
    def _check_protocol_support(cls, device):
        return cls.name in device.support_functions

    # @classmethod
    # def _check_dependencies(cls, device):
    #     for


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

    @classmethod
    def op(cls, *arith_list, **kwargs):
        logger.info(f'param in <FunctionStack>: {kwargs}')
        param_list = kwargs['params']
        print("----------")
        print(arith_list)
        for arith, param in map(lambda x, y: (x, y), arith_list, param_list):
            print(arith, param)
            # todo: 添加try-catch处理
            if not cls._check_protocol_support(arith):
                raise ValueError(f"device {arith} do not support {cls}")
            # 设置设备的stack属性
            if not hasattr(arith, 'stack'):
                setattr(arith, 'stack', cls.init_attrs(arith))
            arith.stack.update(param)
            # 设置interface属性
            # 1.指定参数时
            if 'interface' in param and 'stack_port' in param:
                # 两层map，第一层获得（stack接口，业务接口列表）列表，第二层获得（（stack接口，业务接口）列表
                list1 = map(lambda x, y: map(lambda z: (z, x), y),
                            param['stack_port'], param['interface'])
                list2 = reduce(lambda x, y: x + y, list1)  # 求值,合并列表
                for interface_id, stack_port in list2:
                    # print(interface_id, stack_port)
                    arith.update_attr_to_interface(interface_id=interface_id, stack_port=stack_port)

    @classmethod
    def init_attrs(cls, arith):
        return {
            'enable': True,
            'domain_id': None,
            'member_id': arith.slot_id,
            'priority': 100
        }

    @classmethod
    def validate(cls, devices):
        super().validate(devices)
        if not cls._check_protocol_support(devices):
            raise ProtocolNotSupport("not support FunctionStack")




class ProtocolNotSupport(Exception):
    pass
