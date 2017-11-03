from uniform_model.devices import Device
from uniform_model.templates.base import Template


class ProcessorTemplate(Template):
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