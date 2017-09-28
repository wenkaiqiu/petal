from . import fields

BOOTPROTO_CHOICE = [
    (1, 'none'),
    (2, 'static')
]


class ProtocolType(type):
    def __str__(cls):
        return f'<Protocol: {cls.__name__}>'


class Protocol(metaclass=ProtocolType):
    # todo：感觉没用了
    # @classmethod
    # def interfaces(cls):
    #     return Counter(
    #         map(lambda attr: type(getattr(cls, attr)),
    #             filter(lambda attr: issubclass(type(getattr(cls, attr)), Interface), dir(cls)))
    #     )

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
    bootproto = fields.CharField(choices=BOOTPROTO_CHOICE)
    broadcast = fields.IPField()
    ipaddr = fields.IPField()
    netmask = fields.IPField()
    network = fields.IPField()

    @classmethod
    def op(cls, arith_list):
        print(f'op on {arith_list}')


class ProtocolVLAN(Protocol):
    pass


class ProtocolTrunk(Protocol):
    pass


class ProtocolNotSupport(Exception): pass


class InterfaceNotExist(Exception): pass
