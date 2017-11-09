import logging

from ..devices.device import Device

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.actions.link')
logger.setLevel(logging.DEBUG)


def link(device_a: Device, device_b: Device, link_info):
    logger.info(f'linking {device_a} and {device_b} with {link_info}')
    device_a.link(device_b, link_info)
    device_b.link(device_a, link_info)
    return None  # 错误处理，出错时返回错误
