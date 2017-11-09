import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.server')
logger.setLevel(logging.DEBUG)


class ServerTemplate(Template):
    name = 'server'
    device_vals = {
        'bios_version': False,
        'uri': False,
        'sku': False,
        'serial_number': False,
        'part_number': False,
        'spare_part_number': False,
        'asset_tag': False,
        'hostname': False,
        'hosting_role': False,
        'boot': False,
    }
    model_vals = {
        'manufacturer': False,
        'trusted_modules': False,
    }
    status_vals = {
        'power_state': False,
    }
    inner_rules = tuple()
