import logging

from uniform_model.devices.templates.base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.port')
logger.setLevel(logging.DEBUG)


class PortTemplate(Template):
    name = 'port'
    device_vals = {
        'type': True,
        'interface_type': True,
        'speed': True,
        'unit': True,
        'subcard_number': True,
        'port_number': True,
    }
    model_vals = dict()
    status_vals = dict()
    inner_rules = tuple()

    def generate(cls, info):
        device = super().generate(info)
        device.alias = device.speed + device.unit + ' ' + device.space.serial + '/' + \
                       str(device.subcard_number) + "/" + str(device.port_number)  # 10GE1/0/47
