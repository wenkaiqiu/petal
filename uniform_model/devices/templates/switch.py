import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.switch')
logger.setLevel(logging.DEBUG)


class SwitchTemplate(Template):
    name = 'switch'
    device_vals = {
        'support_functions': False,
        'ports': False,
    }
    model_vals = dict()
    status_vals = dict()
    inner_rules = tuple()


