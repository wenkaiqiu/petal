import logging

from .base import Template

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.ethernet_interface')
logger.setLevel(logging.DEBUG)


class EthernetInterfaceTemplate(Template):
    name = 'ethernet_interface'
    device_vals = {
        'uefi_device_path': False,
        'permanent_mac_address': False,
        'mac_address': False,
        'speed_mbps': False,
        'auto_neg': False,
        'full_duplex': False,
        'hostname': False,
        'fqdn': False,
        'ipv4_addresses': False,
        'ipv6_static_addresses': False,
        'ipv6_default_gateway': False,
    }
    model_vals = {
        'mtu_size': False,
        'max_ipv6_static_addresses': False,
    }
    status_vals = {
        'health_rollup': False,
        'link_state': False,
        'interface_enable': False,
    }
    inner_rules = tuple()
