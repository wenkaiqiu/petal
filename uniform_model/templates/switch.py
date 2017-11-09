import logging

from uniform_model.templates.port import InterfaceManager
from .base import Template
from ..devices.device import Device
# from ..interfaces import InterfaceManager

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.templates.switch')
logger.setLevel(logging.DEBUG)


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
            if item == "ports":
                self._init_ports(device, device_info[item])
            elif item == "support_functions":
                setattr(device, "functions_list", [])
            #     self._init_functions(device, device_info[item])
            setattr(device, item, device_info[item])
            logger.info(f"set attr <{item}> for {self.__class__}: {getattr(device, item)}")
        return device

    def _init_functions(self, device, functions_name):
        logger.info(f"set functions of {self.__class__} device")
        for item in functions_name:
            function_instance = self.function_factory.get_database(item)
            if function_instance is not None:
                setattr(device, item, function_instance)

    def _init_ports(self, device, ports_info):
        logger.info(f"set interfaces of {self.__class__} device")
        for port_info in ports_info:
            InterfaceManager.register_interface_to_device(port_info, device)


