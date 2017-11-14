import logging
from functools import reduce
from itertools import product

from uniform_model.functions.exceptions import ConflictError

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.actions.op')
logger.setLevel(logging.DEBUG)


def op(func, *arith_list, **kwargs):
    """
    配置操作时的流程如下：
    遍历设备列表：
        1. 验证设备是否支持该功能
        2. 实例化function
        3. 检查与设备内的其他功能的依赖冲突.若冲突，则对冲突的功能进行标记，以便进行撤销（由于涉及的规则为检测端口冲突，故解决操作为撤销冲突配置，其他操作未来丰富）
        4. 将实例化function添加到设备功能列表
    :param func: 方法名
    :param arith_list: 设备列表
    :param kwargs: 参数字典
    :return:
    """
    logger.info('<op> start op')
    params = kwargs["params"]
    for index, p in enumerate(arith_list):
        # 1. 验证设备是否支持该功能
        logger.info('check function support')
        # if kwargs['type'] not in p.support_functions:
        #     raise Exception(f'Device {p} is not support function {kwargs["type"]}')
        logger.info(f'<op> configure function <{kwargs["type"]} in {p.model.category} device {p.id}>')
        params[index].update({'device': p})
        # 2. 实例化function
        new_func = func(**params[index])
        # 3. 检查与设备内的其他功能的依赖冲突
        for device_func in p.functions:
            logger.info(f'<op> check {type(new_func)} and {type(device_func)}')
            res = new_func.intra_check(device_func)
            logger.info(f'<op> check result is {res}')
            if not res:
                logger.warning(f'<op> There is a conflict between {new_func.__dict__} and {func.__dict__}')
                device_func.tag = True
        # 4. 将实例化function添加到设备功能列表
        p.functions.append(new_func)
        logger.info('<op> end op')
    return True  # 出错时返回False


def _check_link(*lst):
    # todo: 是否需要检查连接或路径，待确认
    logger.info("<op> check link")
    device_1 = lst[0]
    device_2 = lst[1]
    if all(device_2.id in (link.device_id_a, link.device_id_b) for link in device_1.links):
        return True
    else:
        return False
