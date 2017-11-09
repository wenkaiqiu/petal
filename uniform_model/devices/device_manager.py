import logging

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.device_manager')
logger.setLevel(logging.DEBUG)


class DeviceManager:
    """
    管理已注册的设备实例，与TemplateManager不同，不负责设备实例化。设备实例化由相应Model负责
    """
    __registered_devices = {}

    @classmethod
    def register_device(cls, deivce):
        cls.__registered_devices.update({deivce.id: deivce})
        logger.info(f'register Device <{deivce.id}> success')

    @classmethod
    def list_all_registered(cls):
        return cls.__registered_devices

    @classmethod
    def get_device(cls, device_id):
        return cls.__registered_devices.get(device_id, None)
