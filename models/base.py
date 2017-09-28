import logging

from models.fields import Field
from .protocols import Protocol, InterfaceNotExist
from .interfaces import *

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('model_base')
logger.setLevel(logging.DEBUG)

# TODO: Use trie latter for better performance.
__global_register = set()


def _register_model(cls: object, model_id):
    global __global_register
    identifier = f'{cls.__name__}>>{model_id}'
    if identifier in __global_register: raise ValueError(f'model {identifier} already registered.')
    __global_register.add(identifier)
    logger.info(f'register model {identifier} success')


def list_all_registered():
    return __global_register


class OperableTrait: pass


class ModelType(type):
    def __str__(cls):
        return f'<Model: {cls.__name__}>'

    def __repr__(cls):
        return f'<Model: {cls.__name__}>'


class Model(OperableTrait, metaclass=ModelType):
    def __new__(cls, *args, **kwargs):
        _register_model(cls, args[0])
        return cls

    def __init__(self, logical_id):
        self.logical_id = logical_id

    @classmethod
    def has(cls, interface):
        return interface in cls.interfaces()

    @classmethod
    def interfaces(cls):
        """
        获取Model中的所有Interface对象
        :return: set(<Interface>)
        """
        # return set(filter(lambda x: issubclass(type(x), Interface),
        #                   map(lambda x: getattr(cls, x),
        #                       filter(lambda x: not x.startswith('__'),
        #                              cls.__dict__.keys()))))
        return cls.interface

    @classmethod
    def interface_types(cls):
        """
        获取Model中的所有Interface类型
        :return: set(<InterfaceType>)
        """
        # return set(filter(lambda x: issubclass(x, Interface),
        #                   map(lambda x: type(getattr(cls, x)),
        #                       filter(lambda x: not x.startswith('__'),
        #                              cls.__dict__.keys()))))
        return set(map(lambda x: type(x), cls.interface))


def compatible(*protocols: Protocol, interface_type: str):
    def wrap(model: Model):
        # 检查接口类型
        interfaces_in_model = set(filter(lambda x: type(x).__name__ == interface_type, model.interfaces()))
        if len(interfaces_in_model) == 0:
            raise InterfaceNotExist()
        # 注册各Interface支持的协议类型
        if not hasattr(model, 'support_protocols'):
            setattr(model, 'support_protocols', {})
        getattr(model, 'support_protocols')[interface_type] = protocols
        logger.info(f'<{interface_type}> on <{model.__name__}> support '
                    f'{set(map(lambda x: x.__name__, getattr(model, "support_protocols")[interface_type]))}')
        # 向各Interface对象注册协议支持的属性
        for interface in interfaces_in_model:
            for protocol in protocols:
                [interface.init_attr(x, getattr(protocol, x))
                 for x in filter(lambda attr: issubclass(type(getattr(protocol, attr)), Field), protocol.__dict__.keys())]
        return model

    return wrap


def register_interface(interfaces):
    def register(model: Model):
        model.interface = []
        for item in interfaces:
            if item.get('subcard_number'):
                len_port = len(item['port_number'])
                for i in range(item["num"]):
                    index_1 = i // len_port
                    index_2 = i % len_port
                    temp = item.copy()
                    temp['subcard_number'] = item['subcard_number'][index_1]
                    temp['port_number'] = item['port_number'][index_2]
                    model.interface.append(eval(item['type'] + f"({temp})"))
            else:
                for i in range(item["num"]):
                    temp = item.copy()
                    model.interface.append(eval(item['type'] + f"({temp})"))
        return model
    return register


class ModelGroup(OperableTrait):
    def __init__(self, *args):
        self.group = list(args)

    def __str__(self):
        return f'<Group: {", ".join(map(str, self.group))}>'

    def __repr__(self):
        return f'<Group: {", ".join(map(str, self.group))}>'
