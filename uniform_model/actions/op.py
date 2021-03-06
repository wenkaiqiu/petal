import logging
from functools import reduce
from itertools import product

from ..devices import DeviceGroup
from ..functions import OperableTrait

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('uniform_model.actions.op')
logger.setLevel(logging.DEBUG)


def op(func: OperableTrait, *arith_list, **kwargs):
    lst = [arith.group if isinstance(arith, DeviceGroup) else [arith] for arith in arith_list]
    params = kwargs["params"]
    for index, p in enumerate(reduce(lambda a,b: a+b, lst)):
        # print(p)
        print("---------op-----------")
        print(p.functions_list)
        params[index].update({"device": p})
        p.functions_list.append(func(**params[index]))
        print(p.functions_list)
        # p.functions_list.append()
        # if not _check_link(*p):
        #     return False
        # tag1 = func.op(p[0], **(params[index][0]))
        # tag2 = func.op(p[1], **(params[index][1]))
        # if not tag1 or not tag2:
        #     return False

        # logger.info(f'operate {func} on {p}')
    return True  # 出错时返回False


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
