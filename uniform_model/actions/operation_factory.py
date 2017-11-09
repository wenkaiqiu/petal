import logging
from functools import reduce

from app.factories.base import Factory
from uniform_model import group, DeviceGroup, op
from uniform_model.functions.function_factory import FunctionFactory

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('app.factories.operation_factory')
logger.setLevel(logging.DEBUG)


class OperationFactory(Factory):
    """
    生成op函数,流程如下：
    1. 根据配置参数中的设备ID获取设备实例,并检查是否存在
    2. 检查功能是否已实现
    """

    def generate(self, operation_info, devices):
        logger.info('<OperationFactory> generate operation instance')
        # 1.获取设备实例
        op_devices = [devices.get(device_id, None) for device_id in operation_info['devices']]
        if any(device is None for device in op_devices):
            logger.error(f'device id is not exist in {operation_info}')
            raise Exception(f'device id is not exist in {operation_info}')
        func = FunctionFactory.get_function_model(operation_info["type"])
        if func is None:
            logger.error(f'function type is not exist in {operation_info}')
            raise Exception(f'function type is not exist in {operation_info}')
        return lambda: op(func, *op_devices, **operation_info)
