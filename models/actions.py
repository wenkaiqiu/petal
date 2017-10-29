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
    device_1 = lst[0]
    device_2 = lst[1]
    # print("-----------check_link--------------")
    # print(device_2.id)
    # print(device_1.links)
    # return True
    if device_2.id in device_1.links:
        return True
    else:
        return False


def op(func: OperableTrait, *arith_list, **kwargs):
    lst = [arith.group if isinstance(arith, DeviceGroup) else [arith] for arith in arith_list]
    params = kwargs["params"]
    for index, p in enumerate(product(*lst)):
        if not _check_link(*p):
            return False
        tag1 = func.op(p[0], **(params[index][0]))
        tag2 = func.op(p[1], **(params[index][1]))
        if not tag1 or not tag2:
            return False
        logger.info(f'operate {func} on {p}')
    return True  # 出错时返回False


def group(*devices):
    return DeviceGroup(*devices)
