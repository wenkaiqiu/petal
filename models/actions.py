import logging
from itertools import product

from models.devices import Device, DeviceGroup
from models.functions import OperableTrait

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('actions')
logger.setLevel(logging.DEBUG)


def link(device_a: Device, device_b: Device, link_info):
    logger.info(f'linking {device_a} and {device_b} with {link_info}')
    device_a.link(device_b, link_info)
    device_b.link(device_a, link_info)
    return None  # 错误处理，出错时返回错误


def _check_link(*lst):
    return True


def op(func: OperableTrait, *arith_list, **kwargs):
    print("1111111111111")
    print(arith_list)
    lst = [arith.group if isinstance(arith, DeviceGroup) else [arith] for arith in arith_list]
    print(lst)
    for p in product(*lst):
        if not _check_link(*lst):
            return False
        func.op(p[0], **kwargs)
        func.op(p[1], **kwargs)
        logger.info(f'operate {func} on {p}')
    return True  # 出错时返回False


def group(*devices):
    return DeviceGroup(*devices)
