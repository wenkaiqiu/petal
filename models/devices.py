import logging

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('devices')
logger.setLevel(logging.DEBUG)


class Device:
    def __init__(self, *args, **kwargs):
        self.id = kwargs["id"]
        self.uuid = kwargs["uuid"]
        self.name = kwargs["name"]
        self.model_type = kwargs["model_type"]
        self.links = {}

    def link(self, link_to, link_info):
        link = {
            "name": link_info["name"],
            "id": link_info["id"],
            "to_id": link_to.id,
            "to": link_to,
            "link_type": link_info["link_type"],
            "usage": link_info["usage"]
        }
        self.links.update({link['to_id']: link})


class DeviceGroup:
    def __init__(self, *args):
        self.group = list(args)

    def __str__(self):
        return f'<Group: {", ".join(map(str, self.group))}>'

    def __repr__(self):
        return f'<Group: {", ".join(map(str, self.group))}>'


class DeviceManager:
    """
    管理已注册的设备实例，与ModelManager不同，不负责设备实例化。设备实例化由相应Model负责
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