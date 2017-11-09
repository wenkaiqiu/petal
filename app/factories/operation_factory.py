import logging
from functools import reduce

from app.factories.base import Factory
from app.factories.function_factory import FunctionFactory
from uniform_model import group, DeviceGroup, op

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('app.factories.operation_factory')
logger.setLevel(logging.DEBUG)


class OperationFactory(Factory):
    """
    生成op函数，验证device是否支持该operation
    """

    def generate(self, operation_info, devices):
        logger.info("<OperationFactory> generate operation instance")
        print("operation_info['devices']: " + str(operation_info['devices']))
        # 获取设备实例
        op_devices = list(map(
            lambda x: devices.get(x) if not isinstance(x, list) else group(
                *list(map(lambda y: devices.get(y), x))),
            operation_info['devices']))
        for device in reduce(lambda a, b: a + b,
                             map(lambda y: [y] if not isinstance(y, DeviceGroup) else y.group, op_devices)):
            if device is None:
                return None, f"device which id is {operation_info['device_id_a']} is not exit"
        model = FunctionFactory.get_function_model(operation_info["type"])
        if model is None:
            return None, operation_info["type"]
        return lambda: op(model, *op_devices, **operation_info), None
