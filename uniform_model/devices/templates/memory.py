import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.memory')
logger.setLevel(logging.DEBUG)


class MemoryTemplate(Template):
    name = 'memory'
    device_vals = {
        'uri': False,
        'sku': False,
        'serial_number': False,
        'part_number': False,
        'spare_part_number': False,
        'asset_tag': False,
        'firmware_revision': False,
        'firmware_api_version': False,
        'error_correction': False,
        'operating_speed_mhz': False,
        'volatile_region_size_limit_mib': False,
        'persistent_region_size_limit_mib': False,
        'regions': False,
        'operating_memory_modes': False,
        'is_spare_device_enabled': False,
        'is_rank_spare_enabled': False,
        'volatile_region_number_limit': False,
        'persistent_region_number_limit': False,
        'volatile_region_size_max_mib': False,
        'persistent_region_size_max_mib': False,
        'allocation_increment_mib': False,
        'allocation_alignment_mib': False,
    }
    model_vals = {
        'manufacturer': False,
        'memory_type': False,
        'memory_device_type': False,
        'base_module_type': False,
        'memory_media': False,
        'capacity_mib': False,
        'data_width_bits': False,
        'bus_width_bits': False,
        'allowed_speedsm_hz': False,
        'vendor_id': False,
        'device_id': False,
        'subsystem_vendor_id': False,
        'subsystem_device_id': False,
        'maxtdp_milli_watts': False,
        'security_capabilities': False,
        'spare_device_count': False,
        'rank_count': False,
        'power_management_policy': False,
    }
    status_vals = {
        'health_rollup': False,
    }
    inner_rules = tuple()
