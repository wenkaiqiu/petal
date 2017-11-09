import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.other')
logger.setLevel(logging.DEBUG)


class OtherTemplate(Template):
    name = 'other'
    device_vals = {}
    model_vals = {}
    status_vals = {}
    inner_rules = tuple()
