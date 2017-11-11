import logging

from uniform_model.devices.link_manager import LinkManager
from ..devices.device import Device
from ..devices.link import Link

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.actions.link')
logger.setLevel(logging.DEBUG)


def link(device_a: Device, device_b: Device, link_info):
    """
    连接操作，流程如下：
    1. Link实例化
    2. 检查连接是否重复
    :param device_a: 设备a
    :param device_b: 设备b
    :param link_info: 连接信息
    :return: 是否成功
    """
    logger.info(f'linking {device_a} and {device_b} with {link_info}')
    new_link = Link(**link_info)

    # 检查连接是否重复，由于对称，故只需检查device_a即可
    check_item = ('device_id_a', 'device_id_b', 'port_a', 'port_b')
    if device_a.links:
        for loc_link in device_a.links:
            if all(getattr(new_link,item) in (loc_link.device_id_a, loc_link.device_id_b, loc_link.port_a, loc_link.port_b) for item in check_item):
                loc_link.update(link_info)
                # logger.error(f'repeat link {link_info}')
                # raise ValueError(f'repeat link {link_info}')
    else:
        device_a.links.append(new_link)
        device_b.links.append(new_link)
        LinkManager.regist_link(new_link)
    return True
