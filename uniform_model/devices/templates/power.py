import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.power')
logger.setLevel(logging.DEBUG)


class PowerTemplate(Template):
    name = 'power'
    device_vals = {}
    model_vals = {}
    status_vals = {
        'health_rollup': False,
    }
    inner_rules = tuple()
