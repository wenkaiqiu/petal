import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.pcie')
logger.setLevel(logging.DEBUG)


class PCIeTemplate(Template):
    name = 'pcie'
    device_vals = {
        'sku': False,
        'serial_number': False,
        'part_number': False,
        'spare_part_number': False,
        'asset_tag': False,
    }
    model_vals = {
        'manufacturer': False,
    }
    status_vals = {
        'health_rollup': False,
    }
    inner_rules = tuple()
