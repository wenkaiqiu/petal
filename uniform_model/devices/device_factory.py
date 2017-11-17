import logging

from uniform_model.actions.link_factory import LinkFactory
from uniform_model.devices.templates import *
from uniform_model.functions.function_factory import FunctionFactory

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.device_factory')
logger.setLevel(logging.DEBUG)

# 注册已有设备模型
__global_register = {
    'board': BoardTemplate,
    'chassis': ChassisTemplate,
    'ethernetInterface': EthernetInterfaceTemplate,
    'fan': FanTemplate,
    'manager': ManagerTemplate,
    'memory': MemoryTemplate,
    'other': OtherTemplate,
    'pcie': PCIeTemplate,
    'port': PortTemplate,
    'power': PowerTemplate,
    'processor': ProcessorTemplate,
    'raid': RAIDTemplate,
    'server': ServerTemplate,
    'storage': StorageTemplate,
    'switch': SwitchTemplate,
}


# 获取设备模型，若不存在，返回None
def _get_model_type(model_type):
    global __global_register
    return __global_register.get(model_type, None)


class DeviceFactory:
    def generate(self, device_info):
        """
        根据Model生成Device
        :param device_info:
        :return:
        """
        logger.info(f'<DeviceFactory> generate device instance with info {device_info}')
        device = _get_model_type(device_info['model_type']).generate(device_info)
        # 若设备含有功能，则对其配置功能
        if hasattr(device, 'support_functions') and 'functions' in device_info:
            for item in device_info['functions']:
                item['params'].update({'device': device, 'id': item['id']})
                device.functions.append(FunctionFactory().generate(item['type'], item['params']))
        return device
