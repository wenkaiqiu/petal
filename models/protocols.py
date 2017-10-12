from collections import Counter
from functools import reduce

from models.interfaces import Interface


class ProtocolType(type):
    def __str__(cls):
        return f'<Protocol: {cls.__name__}>'


class Protocol(metaclass=ProtocolType):
    @classmethod
    def interfaces(cls):
        return Counter(
            map(lambda attr: type(getattr(cls, attr)),
                filter(lambda attr: issubclass(type(getattr(cls, attr)), Interface), dir(cls)))
        )

    # noinspection PyUnusedLocal
    @classmethod
    def validate(cls, model):
        """
        自定义协议和模型检查流程，在接口检查后自动调用
        :return: 检查通过返回真，否则 raise对应错误(推荐) 或者 返回False
        """
        return True

    @classmethod
    def op(cls, arith_list): raise NotImplemented()


class ProtocolIP(Protocol):
    attrs = ['bootproto', 'broadcast', 'ipaddr', 'netmask', 'network']

    @classmethod
    def op(cls, arith_list):
        print(f'op on {arith_list}')


class ProtocolVLAN(Protocol):
    @classmethod
    def op(cls, arith_list):
        print(f'op on {arith_list}')


class ProtocolTrunk(Protocol):
    @classmethod
    def op(cls, arith_list):
        print(f'op on {arith_list}')


class ProtocolStack(Protocol):
    @classmethod
    def op(cls, arith_list, **kwargs):
        print(f'param: {kwargs}')
        param = kwargs['params']
        count = 0
        for arith in arith_list:
            # 设置stack属性
            if not hasattr(arith, 'stack'):
                setattr(arith, 'stack', cls.init_param(arith))
            arith.stack.update(param[count])
            # 设置interface属性
            # 指定参数时
            if 'interface' in param[count] and 'stack_port' in param[count]:
                # 两层map，第一层获得（stack接口，业务接口列表）列表，第二层获得（（stack接口，业务接口）列表
                list1 = map(lambda x, y: list(map(lambda z: (z, x), y)),
                            param[count]['stack_port'], param[count]['interface'])
                list2 = reduce(lambda x, y: x + y, list1)  # 求值,合并列表
                for item in list2:
                    arith.update_interface(port_id=item[0], stack_port=item[1])
            count += 1

    @classmethod
    def init_param(cls, arith):
        return {
            'enable': True,
            'domain_id': None,
            'member_id': arith.slot_id,
            'priority': 100
        }


class ProtocolNotSupport(Exception): pass
