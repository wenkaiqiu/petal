import logging

from .base import Template
from ..devices.device import Device

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('uniform_model.templates.other')
logger.setLevel(logging.DEBUG)


class OtherTemplate(Template):
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
