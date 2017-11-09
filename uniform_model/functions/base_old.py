import logging

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.functions.base')
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
                raise ProtocolNotSupport(f'device {device.id} not support FunctionStack')
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
        return all(getattr(device, dependency).enable
                   for dependency in cls.dependencies)

    def generate_conf(self): raise NotImplementedError()

    def generate_revoke_conf(self): raise NotImplementedError()


class ProtocolNotSupport(Exception): pass
