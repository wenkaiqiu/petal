import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.storage')
logger.setLevel(logging.DEBUG)


class StorageTemplate(Template):
    name = 'storage'
    device_vals = {}
    model_vals = {}
    status_vals = {}
    inner_rules = tuple()
