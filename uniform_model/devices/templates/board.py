import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.board')
logger.setLevel(logging.DEBUG)


class BoardTemplate(Template):
    name = 'board'
    device_vals = {
        'sku': False,
        'serial_number': False,
        'part_number': False,
        'spare_part_number': False,
        'asset_tag': False,
        'card_no': False,
        'device_locator': False,
        'location': False,
        'board_name': False,
        'board_id': False,
        'manufacture_date': False,
    }
    model_vals = {
        'manufacturer': False,
        'device_type': False,
        'cpld_version': False,
    }
    status_vals = {
        'health_rollup': False,
    }
    inner_rules = tuple()
