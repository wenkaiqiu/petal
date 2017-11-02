import logging

from ..devices.device_manager import DeviceManager

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('uniform_model.templates.base')
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
