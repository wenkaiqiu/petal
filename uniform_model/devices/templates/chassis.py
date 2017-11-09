import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.chassis')
logger.setLevel(logging.DEBUG)


class ChassisTemplate(Template):
    name = 'chassis'
    device_vals = {
        'sku': False,
        'serial_number': False,
        'part_number': False,
        'spare_part_number': False,
        'indicator_led': False,
        'height_mm': False,
        'width_mm': False,
        'depth_mm': False,
        'weight_kg': False,
    }
    model_vals = {
        'manufacturer': False,
        'chassis_type': False,
    }
    status_vals = {
        'health_rollup': False,
        'power_state': False,
    }
    inner_rules = tuple()