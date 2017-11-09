import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.raid')
logger.setLevel(logging.DEBUG)


class RAIDTemplate(Template):
    name = 'raid'
    device_vals = {
        'sku': False,
        'serial_number': False,
        'part_number': False,
        'spare_part_number': False,
        'asset_tag': False,
        'member_id': False,
        'firmware_version': False,
        'speed_gbps': False,
    }
    model_vals = {
        'manufacturer': False,
    }
    status_vals = {
        'health_rollup': False,
    }
    inner_rules = tuple()
