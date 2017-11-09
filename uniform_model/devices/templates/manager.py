import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.manager')
logger.setLevel(logging.DEBUG)


class ManagerTemplate(Template):
    name = 'manager'
    device_vals = {
        'firmware_version': False,
        'service_entry_point_uuid': False,
        'date_time': False,
        'date_time_local_offset': False,
    }
    model_vals = {
        'manager_type': False,
    }
    status_vals = {
        'health_rollup': False,
        'power_state': False,
    }
    inner_rules = tuple()
