import logging
from itertools import chain

from models.devices import Device, DeviceManager
from models.interfaces import InterfaceManager

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('models')
logger.setLevel(logging.DEBUG)


class TemplateType(type):
    def __str__(cls):
        return f'<Model: {cls.__name__}>'

    def __repr__(cls):
        return f'<Model: {cls.__name__}>'


class Template(metaclass=TemplateType):
    @classmethod
    def set_device_conf(cls, device_conf):
        logger.info("configure <Model>")
        # 用于检查创建device的必要属性
        cls.device_conf = list(filter(lambda x: device_conf[x], device_conf))

    def __init__(self, *args, **kwargs):
        self.model_type = kwargs["model_type"]
        self.name = kwargs["name"]
        self.category = kwargs["category"]
        self.properties_init = kwargs["properties"]
        self.properties = list(filter(lambda x: self.properties_init[x], self.properties_init))
        from app.factories import FunctionFactory
        self.function_factory = FunctionFactory()

    def generate(self, device_info):
        logger.info(f"{self.__class__} generate")
        lack = self._check_device_info(device_info)
        if lack:
            logger.info(f"lack attribute {lack} for generate {self.__class__}")
            raise AttributeError(f"lack attribute {lack} for generate {self.__class__}")
        device = self.generate_device(device_info)
        DeviceManager.register_device(device)
        return device

    def _check_device_info(self, device_info):
        logger.info(f"checking {self.__class__} device info")
        lack = []
        for item in self.device_conf:
            if item not in device_info:
                lack.append(item)
        return lack

    def generate_device(self, device_info):
        pass


class ChasisTemplate(Template):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _check_device_info(self, device_info):
        lack = super()._check_device_info(device_info)
        for item in self.properties:
            if item not in device_info:
                lack.append(item)
        return lack

    def generate_device(self, device_info):
        device = Device(**device_info)
        return device


class SwitchTemplate(Template):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _check_device_info(self, device_info):
        lack = super()._check_device_info(device_info)
        for item in self.properties:
            if item not in device_info:
                lack.append(item)
        return lack

    def generate_device(self, device_info):
        logger.info(f"generate {self.__class__} device")
        device = Device(**device_info)
        logger.info(f"set attrs of {self.__class__} device")
        for item in filter(lambda x: x not in self.device_conf, self.properties):
            if item == "support_functions":
                self._init_functions(device, device_info[item])
            elif item == "ports":
                self._init_ports(device, device_info[item])
            setattr(device, item, device_info[item])
            logger.info(f"set attr <{item}> for {self.__class__}: {getattr(device, item)}")
        return device

    def _init_functions(self, device, functions_name):
        logger.info(f"set functions of {self.__class__} device")
        for item in functions_name:
            function_instance = self.function_factory.generate(item)
            if function_instance is not None:
                setattr(device, item, function_instance)

    def _init_ports(self, device, ports_info):
        logger.info(f"set interfaces of {self.__class__} device")
        for port_info in ports_info:
            InterfaceManager.register_interface_to_device(port_info, device)


# 注册已有设备模型
__global_register = {
    "chasis": ChasisTemplate,
    "switch": SwitchTemplate
}


# 获取设备模型，若不存在，返回None
def _get_model_type(model_type):
    global __global_register
    return __global_register.get(model_type, None)


class ModelManager:
    """
    负责Model的实例化，并管理已注册的模型实例
    """
    __registered_models = {}

    @classmethod
    def _check_info(cls, model_info):
        if "model_type" not in model_info:
            raise NameError("<model_type> is needed in model_info")
        model_type = model_info["model_type"]
        for item in chain(cls.conf["base"], cls.conf[model_type]):
            if item not in model_info:
                raise NameError(f"<{item}> is needed in model_info")

    @classmethod
    def set_conf(cls, conf):
        logger.info("<ModelManager> set_conf")
        cls.conf = {"base": filter(lambda x: conf[x], conf)}
        for item in filter(lambda x: x.startswith("other"), conf):
            cls.conf.update({item.split("_")[1]: filter(lambda x: conf[item][x], conf[item])})

    @classmethod
    def register_model(cls, model_info):
        try:
            cls._check_info(model_info)
            logger.info(f"model <{model_info['name']}> checked success")
        except NameError as e:
            print(e)

        model_type = model_info["model_type"]
        model = _get_model_type(model_type)(**model_info)
        # 检查该类型Model是否重复注册
        if cls.get_model(model.name) is not None:
            raise ValueError(f'model <{model.name}> already registered.')
        cls.__registered_models.update({model.name: model})
        logger.info(f'register model <{model.name}> success')

    @classmethod
    def list_all_registered(cls):
        return cls.__registered_models

    @classmethod
    def get_model(cls, model_name):
        return cls.__registered_models.get(model_name, None)
