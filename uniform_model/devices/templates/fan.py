import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.fan')
logger.setLevel(logging.DEBUG)


class FanTemplate(Template):
    name = 'fan'
    device_vals = {
        'sku': False,
        'serial_number': False,
        'part_number': False,
        'spare_part_number': False,
        'indicator_led': False,
        'reading_units': False,
        'physical_context': False,
        'member_id': False,
    }
    model_vals = {
        'manufacturer': False,
        'lower_threshold_fatal': False,
        'lower_threshold_critical': False,
        'lower_threshold_non_critical': False,
        'upper_threshold_fatal': False,
        'upper_threshold_critical': False,
        'upper_threshold_non_critical': False,
    }
    status_vals = {
        'health_rollup': False,
    }
    inner_rules = tuple()
