from models.interfaces import InterfaceRJ45, Interface
from collections import Counter


class BaseProtocol:
    @classmethod
    def interfaces(cls):
        return Counter(
            map(lambda attr: type(getattr(cls, attr)),
                filter(lambda attr: issubclass(type(getattr(cls, attr)), Interface), dir(cls)))
        )

    def __str__(self):
        return f'{type(self).__name__}'

    # noinspection PyUnusedLocal
    @classmethod
    def validate(cls, model):
        """
        自定义协议和模型检查流程，在接口检查后自动调用
        :return: 检查通过返回真，否则 raise对应错误(推荐) 或者 返回False
        """
        return True


class ProtocolIP(BaseProtocol):
    a = InterfaceRJ45()


class ProtocolVLAN(BaseProtocol):
    a = ProtocolIP()


class ProtocolTrunk(BaseProtocol):
    a = InterfaceRJ45()
    b = InterfaceRJ45()


class ProtocolNotSupport(Exception): pass
