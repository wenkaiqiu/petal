import logging

from uniform_model.devices.templates.base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.processor')
logger.setLevel(logging.DEBUG)


class ProcessorTemplate(Template):
    name = 'processor'
    device_vals = {
        'processor_id': False,
        'socket': False,
        'sku': False,
        'serial_number': False,
        'part_number': False,
        'spare_part_number': False,
        'asset_tag': False,
    }
    model_vals = {
        'processor_type': False,
        'processor_architecture': False,
        'manufacturer': False,
        'instruction_set': False,
        'max_speedm_hz': False,
        'total_cores': False,
        'total_threads': False,
    }
    status_vals = {
        'health_rollup': False,
    }
    inner_rules = tuple()